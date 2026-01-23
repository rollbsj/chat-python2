import requests
from bs4 import BeautifulSoup

response = requests.get("https://search.incruit.com/list/search.asp?col=job&kw=%B1%B8%B9%CC%BD%C3+cad")
#print(response.text)
soup = BeautifulSoup(response.text, "html.parser")
print(soup)