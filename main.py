from bs4 import BeautifulSoup
import requests
import pandas as pd

baseurl = 'https://www.alternate.de'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'
}

# get product links
r = requests.get('https://www.alternate.de/Grafikkarten/html/listings/1458222035317/1486466143032?lk=8378&size=500&hideFilter=false&showFilter=false&filter_2203=NVIDIA+GeForce+RTX+3080&filter_2203=NVIDIA+GeForce+RTX+3070', headers=headers)
soup = BeautifulSoup(r.content, 'lxml')

productlist = soup.find_all('div', class_='listRow')

productlinks = []

for item in productlist:
    for link in item.find_all('a', class_='productLink', href=True):
        productlinks.append(baseurl + link['href'])

# get product information
counter = 0
rtxlist = []
for link in productlinks:
    r = requests.get(link, headers=headers)
    soup = BeautifulSoup(r.content, 'lxml')

    # get product name
    nav_tag = soup.find('nav', class_='breadCrumbs')
    last_span = None
    for last_span in nav_tag:
        pass
    if last_span:
        productname = last_span.strip()
    else:
        productname = 'N\\A'

    # get product price
    price = soup.find('div', class_='price')['data-standard-price']

    # get availability
    stock = soup.find('div', class_='availability').text.strip()

    # save data

    item = {
        'Name': productname,
        'Price': price,
        'Stock': stock
    }

    print('Saving:')
    print('Item ', counter, ': ', productname, ', Price: ', price, '€, Stock: ', stock)
    rtxlist.append(item)
    counter += 1

# save to pandas dataframe
df = pd.DataFrame(rtxlist)
df.to_excel('alternateRTX.xlsx')
print(df)
input('Press Enter to exit...')
