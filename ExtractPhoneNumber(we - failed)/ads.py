import requests
from bs4 import BeautifulSoup
import csv





base_url = 'https://www.storia.ro/ro/rezultate/vanzare/apartament/toata-romania?market=ALL&viewType=listing'
response = requests.get(base_url)
soup = BeautifulSoup(response.content, 'html.parser')


print(soup)
