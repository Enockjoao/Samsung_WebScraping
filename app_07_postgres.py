import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
import asyncio
from telegram import Bot
import os
from dotenv import load_dotenv
import psycopg2
from sqlalchemy import create_engine

load_dotenv()

# Configurações do bot do Telegram
TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
bot = Bot(token=TOKEN)

# Configurações do banco de dados PostgreSQL
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")

# Cria o engine do SQLAlchemy para o PostgreSQL
DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
engine = create_engine(DATABASE_URL)


def fetch_page():
    url="https://www.mercadolivre.com.br/samsung-galaxy-s23-ultra-5g-dual-sim-256-gb-preto-12-gb-ram/p/MLB24594025?pdp_filters=item_id%3AMLB3555298458&from=gshop&matt_tool=35422514&matt_word=&matt_source=google&matt_campaign_id=14303413643&matt_ad_group_id=125984291437&matt_match_type=&matt_network=g&matt_device=c&matt_creative=539354956512&matt_keyword=&matt_ad_position=&matt_ad_type=pla&matt_merchant_id=735128188&matt_product_id=MLB24594025-product&matt_product_partition_id=2365693158465&matt_target_id=pla-2365693158465&cq_src=google_ads&cq_cmp=14303413643&cq_net=g&cq_plt=gp&cq_med=pla&gad_source=1&gclid=CjwKCAiA9bq6BhAKEiwAH6bqoPFG-6eVBg5uzJm4cDLPMC2Bh-ZHxfqtM42UGeyASqSEZXZU1q8rIxoCi-oQAvD_BwE"
    response = requests.get(url)
    return(response.text)

"""Faz o request no Site e pega os dados como : Preços e nome do produto """
def parse_page(html):
    soup = BeautifulSoup(html, 'html.parser')
    product_name = soup.find('h1', class_='ui-pdp-title').get_text(strip=True)
    prices = soup.find_all('span', class_='andes-money-amount__fraction')
    old_price = int(prices[0].get_text(strip=True).replace('.', ''))
    new_price = int(prices[1].get_text(strip=True).replace('.', ''))
    installment_price = int(prices[2].get_text(strip=True).replace('.', ''))

    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')

    return {
        'product_name': product_name,
        'old_price': old_price,
        'new_price': new_price,
        'installment_price': installment_price,
        'timestamp': timestamp
    }

def create_connection():
    """Cria uma conexão com o banco de dados PostgreSQL."""
    conn = psycopg2.connect(
        dbname=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        host=POSTGRES_HOST,
        port=POSTGRES_PORT
    )
    return conn

def setup_database(conn):
    """Cria a tabela de preços se ela não existir."""
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS prices (
            id SERIAL PRIMARY KEY,
            product_name TEXT,
            old_price INTEGER,
            new_price INTEGER,
            installment_price INTEGER,
            timestamp TIMESTAMP
        )
    ''')
    conn.commit()
    cursor.close()

def save_to_database(data, table_name='prices'):
    """Salva uma linha de dados no banco de dados PostgreSQL usando pandas e SQLAlchemy."""
    df = pd.DataFrame([data])
    # Usa SQLAlchemy para salvar os dados no PostgreSQL
    df.to_sql(table_name, engine, if_exists='append', index=False)

def get_max_price(conn):
    """Consulta o maior preço registrado até o momento com o timestamp correspondente."""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT new_price, timestamp 
        FROM prices 
        WHERE new_price = (SELECT MAX(new_price) FROM prices);
    """)
    result = cursor.fetchone()
    cursor.close()
    if result and result[0] is not None:
        return result[0], result[1]
    return None, None

async def send_telegram_message(text):
    """Envia uma mensagem para o Telegram."""
    await bot.send_message(chat_id=CHAT_ID, text=text)

async def main():
    conn = create_connection()
    setup_database(conn)

    try:
        while True:
            # Faz a requisição e parseia a página
            page_content = fetch_page()
            product_info = parse_page(page_content)
            current_price = product_info['new_price']
            
            # Obtém o maior preço já salvo
            max_price, max_price_timestamp = get_max_price(conn)
            
            # Comparação de preços
            if max_price is None or current_price > max_price:
                message = f"Novo preço maior detectado: {current_price}"
                print(message)
                await send_telegram_message(message)
                max_price = current_price
                max_price_timestamp = product_info['timestamp']
            else:
                message = f"O maior preço registrado é {max_price} em {max_price_timestamp}"
                print(message)
                await send_telegram_message(message)

            # Salva os dados no banco de dados PostgreSQL
            save_to_database(product_info)
            print("Dados salvos no banco:", product_info)
            
            # Aguarda 10 segundos antes da próxima execução
            await asyncio.sleep(10)

    except KeyboardInterrupt:
        print("Parando a execução...")
    finally:
        conn.close()

# Executa o loop assíncrono
asyncio.run(main())