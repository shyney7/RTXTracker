from bs4 import BeautifulSoup
from requests_html import HTMLSession
import pandas as pd

s = HTMLSession()

# get html func
def getdata(url):
    r = s.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup


# ---scrap alternate.de---
baseurl = 'https://www.alternate.de'


# get product links
url = 'https://www.alternate.de/Grafikkarten/html/listings/1458222035317/1486466143032?lk=8378&size=500&hideFilter=false&showFilter=false&filter_2203=NVIDIA+GeForce+RTX+3080&filter_2203=NVIDIA+GeForce+RTX+3070'
soup = getdata(url)

productlist = soup.find_all('div', class_='listRow')

productlinks = []

for item in productlist:
    for link in item.find_all('a', class_='productLink', href=True):
        productlinks.append(baseurl + link['href'])

# get product information
counter = 0
rtxlist = []
for link in productlinks:
    soup = getdata(link)

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
        'Stock': stock,
        'Link': link
    }

    print('Saving:')
    print('Item ', counter, ': ', productname, ', Price: ', price, '€, Stock: ', stock)
    rtxlist.append(item)
    counter += 1

# save to pandas dataframe
df = pd.DataFrame(rtxlist)
df.to_csv('alternateRTX.csv')
print(df)


# ---scrape caseking---
# RTX3080
# get product links
url = 'https://www.caseking.de/pc-komponenten/grafikkarten?ckFilters=13915&ckTab=0&sPage=1&sPerPage=48'
soup = getdata(url)

productlinks = soup.find_all('a', class_='buynow no-modal', href=True)
links = []
for link in productlinks:
    links.append(link['href'])

name = soup.find_all('span', class_='ProductTitle')
price = soup.find_all('span', class_='price')
stock = soup.find_all('span', class_='frontend_plugins_index_delivery_informations')

counter = 0
rtxlist = []
for link in links:
    item = {
        'Name': name[counter].text.strip(),
        'Price': price[counter].text.replace('€', '').replace('.', '').replace(',', '.').replace('*', '').strip(),
        'Stock': stock[counter].text.strip(),
        'Link': link
    }
    print('Saving Item ', counter, ':')
    print(item)
    rtxlist.append(item)
    counter += 1


# RTX 3070
url = 'https://www.caseking.de/pc-komponenten/grafikkarten?ckFilters=13917&ckTab=0&sPage=1&sPerPage=48'
soup = getdata(url)

productlinks = soup.find_all('a', class_='buynow no-modal', href=True)
links = []
for link in productlinks:
    links.append(link['href'])

name = soup.find_all('span', class_='ProductTitle')
price = soup.find_all('span', class_='price')
stock = soup.find_all('span', class_='frontend_plugins_index_delivery_informations')

counter = 0
for link in links:
    item = {
        'Name': name[counter].text.strip(),
        'Price': price[counter].text.replace('€', '').replace('.', '').replace(',', '.').replace('*', '').strip(),
        'Stock': stock[counter].text.strip(),
        'Link': link
    }
    print('Saving Item ', counter, ':')
    print(item)
    rtxlist.append(item)
    counter += 1


# save to pandas dataframe
df = pd.DataFrame(rtxlist)
print(df)
df.to_csv('casekingRTX.csv')
input('Press Enter to exit...')
