import requests
from bs4 import BeautifulSoup
import time
import pandas as pd

def fetch_page():
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

def save_to_dataframe(product_info, df):
    new_row = pd.DataFrame([product_info])
    """Salva uma linha de dados no banco de dados SQLite usando Pandas. """
    df = pd.concat([df, new_row], ignore_index=True)
    return df
"""Teste de Funções """
if __name__ == "__main__":
    """ Data Frame Para Acumular os resultados """
    df = pd.DataFrame()

    url="https://www.mercadolivre.com.br/samsung-galaxy-s23-ultra-5g-dual-sim-256-gb-preto-12-gb-ram/p/MLB24594025?pdp_filters=item_id%3AMLB3555298458&from=gshop&matt_tool=35422514&matt_word=&matt_source=google&matt_campaign_id=14303413643&matt_ad_group_id=125984291437&matt_match_type=&matt_network=g&matt_device=c&matt_creative=539354956512&matt_keyword=&matt_ad_position=&matt_ad_type=pla&matt_merchant_id=735128188&matt_product_id=MLB24594025-product&matt_product_partition_id=2365693158465&matt_target_id=pla-2365693158465&cq_src=google_ads&cq_cmp=14303413643&cq_net=g&cq_plt=gp&cq_med=pla&gad_source=1&gclid=CjwKCAiA9bq6BhAKEiwAH6bqoPFG-6eVBg5uzJm4cDLPMC2Bh-ZHxfqtM42UGeyASqSEZXZU1q8rIxoCi-oQAvD_BwE"
    while True:
        page_content = fetch_page()
        produto_info = parse_page(page_content)
        df = save_to_dataframe(produto_info, df)
        print(df)
        time.sleep(10)