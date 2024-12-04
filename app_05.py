import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
import sqlite3

def fetch_page():
    url="https://www.mercadolivre.com.br/samsung-galaxy-s23-ultra-5g-dual-sim-256-gb-preto-12-gb-ram/p/MLB24594025?pdp_filters=item_id%3AMLB3555298458&from=gshop&matt_tool=35422514&matt_word=&matt_source=google&matt_campaign_id=14303413643&matt_ad_group_id=125984291437&matt_match_type=&matt_network=g&matt_device=c&matt_creative=539354956512&matt_keyword=&matt_ad_position=&matt_ad_type=pla&matt_merchant_id=735128188&matt_product_id=MLB24594025-product&matt_product_partition_id=2365693158465&matt_target_id=pla-2365693158465&cq_src=google_ads&cq_cmp=14303413643&cq_net=g&cq_plt=gp&cq_med=pla&gad_source=1&gclid=CjwKCAiA9bq6BhAKEiwAH6bqoPFG-6eVBg5uzJm4cDLPMC2Bh-ZHxfqtM42UGeyASqSEZXZU1q8rIxoCi-oQAvD_BwE"
    response = requests.get(url)
    return(response.text)
"""Faz o request no Site e pega os dados como : Preços e nome do produto """
def parse_page(html):
    soup = BeautifulSoup(html, 'html.parser')
    product_name = soup.find('h1', class_='ui-pdp-title').get_text()
    prices = soup.find_all('span', class_='andes-money-amount__fraction')
    old_price: int = int(prices[0].get_text().replace('.', ''))
    new_price: int = int(prices[1].get_text().replace('.', ''))
    installment_price: int = int(prices[2].get_text().replace('.', ''))

    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')

    return {
        'product_name': product_name,
        'old_price': old_price,
        'new_price': new_price,
        'installment_prices': installment_price,
        'timestamp': timestamp
    }

def create_connection(db_name='S24_prices.db'):
    '''Cria um banco de dados SQLite'''
    conn = sqlite3.connect(db_name)
    return conn

def setup_database(conn):
    '''Cria a tabela de preços se ela não existir'''
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS prices (
            id  INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name TEXT,
            old_price INTEGER,
            new_price INTEGER,
            installment_prices INTEGER,
            timestamp TEXT
        )
    ''')
    conn.commit()

def save_to_database(conn, data):
    """Salva uma linha de dados no banco de dados SQLite usando Pandas. """
    new_row = pd.DataFrame([data])#converte o dicionário em um Dataframe de uma Linha
    new_row.to_sql('prices', conn, if_exists='append', index=False) # Salva no banco de dados

def get_max_price(conn):
    #Conectar com meu banco
    cursor = conn.cursor()
    #O preço máximo historico (SELECT max(Price).....)
    cursor.execute("SELECT MAX(new_price), timestamp FROM prices")
    #Retorna esse valor
    result = cursor.fetchone()
    return result[0], result[1]



"""Teste de Funções """
if __name__ == "__main__":
    '''Configuração do Banco de Dados'''
    conn = create_connection()
    setup_database(conn)

    while True:
        """Faz a requisição e parseia a Pag"""
        page_content = fetch_page()
        product_info = parse_page(page_content)
        current_price = product_info["new_price"]

        max_price, max_price_timestamp = get_max_price(conn)    


        if current_price > max_price:
            print("Preço maior detectado")
            max_price = current_price
            max_price_timestamp = product_info['timestamp']
        else:
            print(f"O maior preço registrado é {max_price} em {max_price_timestamp}")

        """Salva os dados no Banco de dados SQLite"""
        save_to_database(conn, product_info)
        print("Dados Salvos no Banco:", product_info)

        """Aguarda 10 Seg antes da Prox Execução"""
        time.sleep(10)