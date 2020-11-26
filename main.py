from bs4 import BeautifulSoup
import requests

baseurl = 'https://www.alternate.de/'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'
}

r = requests.get('https://www.alternate.de/Grafikkarten/html/listings/1458222035317/1486466143032?lk=8378&size=500&hideFilter=false&showFilter=false&filter_2203=NVIDIA+GeForce+RTX+3080&filter_2203=NVIDIA+GeForce+RTX+3070')
soup = BeautifulSoup(r.content, 'lxml')

productlist = soup.find_all('div', class_='listRow')

productlinks = []

for item in productlist:
    for link in item.find_all('a', class_='productLink', href=True):
        print(link['href'])
