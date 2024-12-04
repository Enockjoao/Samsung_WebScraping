# Monitoramento de Preços do Mercado Livre

Este projeto é um **web scraper** que monitora o preço de um produto específico no Mercado Livre, armazena os dados em um banco de dados SQLite e envia notificações via Telegram quando detecta mudanças de preço significativas.

---

## 🚀 Funcionalidades

- **Coleta automática**:
  - Faz requisições ao Mercado Livre para obter o preço atual de um produto.
  - Extrai informações do nome do produto, preço antigo, preço atual e preço parcelado.
  
- **Armazenamento**:
  - Salva os dados coletados em um banco de dados SQLite para análise futura.
  - Armazena o maior preço já registrado com a data e hora.

- **Notificações**:
  - Envia mensagens via Telegram se o preço atual for maior que o maior preço histórico.

---

## 🛠️ Tecnologias Utilizadas

- **Python**:
  - `requests`: Para requisições HTTP.
  - `BeautifulSoup` (do `bs4`): Para análise e extração de dados HTML.
  - `sqlite3`: Para gerenciamento do banco de dados.
  - `pandas`: Para manipulação de dados.
  - `telegram.Bot`: Para integração com o Telegram.
  - `dotenv`: Para carregar variáveis de ambiente.

---

## 📦 Requisitos

1. **Python 3.9+**.
2. **Bibliotecas necessárias** (instale via `pip`):
   ```bash
   pip install requests beautifulsoup4 pandas python-telegram-bot python-dotenv
Configuração do Telegram:

Crie um bot usando o BotFather no Telegram.
Obtenha o TOKEN do bot e o CHAT_ID para onde as mensagens serão enviadas.
Arquivo .env:

Crie um arquivo .env na raiz do projeto com o seguinte formato:
makefile
 ```TELEGRAM_TOKEN=seu_token_aqui
 ```TELEGRAM_CHAT_ID=seu_chat_id_aqui


📖 Como usar

Clone o repositório:
bash
 ```git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio


Configure as dependências:
bash
 ```pip install -r requirements.txt

Execute o script:
bash
 ```python main.py

⚙️ Estrutura do Projeto
plaintext

 ```.
 ```├── main.py          # Script principal
 ```├── requirements.txt # Dependências do projeto
 ```├── .env             # Variáveis de ambiente (não commitado)
 ```├── S24_prices.db    # Banco de dados SQLite (gerado pelo script)
 ```├── README.md        # Este arquivo


🛠️ Melhorias Futuras
Adicionar tratamento de erros para conexões falhas ou alterações no layout do site.
Tornar o intervalo de verificação configurável.
Adicionar suporte para múltiplos produtos.
Monitorar também a queda nos preços.


📝 Observações
Este projeto é destinado a fins educacionais e pessoais.
Certifique-se de respeitar os termos de uso do Mercado Livre ao usar este scraper.


👤 Autor
Enock
Estudante e desenvolvedor entusiasta.


📄 Licença
Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

markdown








