import requests
from pprint import pprint
import json

isbn = 9788577790104
link = f'https://brasilapi.com.br/api/isbn/v1/{isbn}'
acesso = requests.get(link)
print(acesso.encoding)
dados = acesso.json()
print(dados['author'])
