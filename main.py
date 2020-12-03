from bs4 import BeautifulSoup
from requests_html import HTMLSession
import pandas as pd

s = HTMLSession()


# get html func
def getdata(url):
    r = s.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup


# Alternate get data func
def get_alternate_data(soup):
    baseurl = 'https://www.alternate.de'
    productlist = soup.find_all('div', class_='listRow')

    productlinks = []
    for item in productlist:
        for link in item.find_all('a', class_='productLink', href=True):
            productlinks.append(baseurl + link['href'])

    names = soup.find_all('a', class_='productLink')

    stock_span = soup.find_all('span', class_='stockStatusContainer complete')
    stock = []
    for item in stock_span:
        stock.append(item.find('strong').text.strip())

    prices = soup.find_all('span', class_='price right right10')

    rtxlist = []
    counter = 0
    for link in productlinks:
        item = {
            'Name': names[counter]['title'],
            'Price': prices[counter].text.replace('€', '').replace('.', '').replace(',', '.').replace('-', '0').replace('*', '').strip(),
            'Stock': stock[counter],
            'Link': link
        }
        print('Saving Item ', counter, ':')
        print(item)
        rtxlist.append(item)
        counter += 1
    return rtxlist


# Caseking get data func
def get_ck_data(soup):
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
    return rtxlist


# acom-pc get data func
def get_acomp_data(soup):
    productlinks = []
    names = []
    stock = []
    rtxlist = []

    productlist = soup.find_all('div', class_='product-content-inner left')

    for item in productlist:
        for link in item.find_all('a', href=True):
            productlinks.append(link['href'])
        for name in item.find_all('a'):
            names.append(name.text.strip())

    price = soup.find_all('span', class_='price')

    stockdiv = soup.find_all('div', class_='filial_stock_list')
    for item in stockdiv:
        stock.append(item.find('span').text.strip())

    counter = 0
    for link in productlinks:
        item = {
            'Name': names[counter],
            'Price': price[counter].text.replace('EUR', '').replace('.', '').replace(',', '.').strip(),
            'Stock': stock[counter],
            'Link': link
        }
        print('Saving Item ', counter, ':')
        print(item)
        rtxlist.append(item)
        counter += 1
    return rtxlist

# Alternate 3070 & 3080
url = 'https://www.alternate.de/Grafikkarten/html/listings/1458222035317/1486466143032?lk=8378&size=500&hideFilter=false&showFilter=false&filter_2203=NVIDIA+GeForce+RTX+3080&filter_2203=NVIDIA+GeForce+RTX+3070'
soup = getdata(url)

rtxlist = []
rtxlist.extend(get_alternate_data(soup))

# save to pandas dataframe
df = pd.DataFrame(rtxlist)
df.to_csv('alternateRTX.csv')
print(df)


# Caseking RTX3080
url = 'https://www.caseking.de/pc-komponenten/grafikkarten?ckFilters=13915&ckTab=0&sPage=1&sPerPage=48'
soup = getdata(url)
rtxlist = []

rtxlist.extend(get_ck_data(soup))

# Caseking RTX 3070
url = 'https://www.caseking.de/pc-komponenten/grafikkarten?ckFilters=13917&ckTab=0&sPage=1&sPerPage=48'
soup = getdata(url)

rtxlist.extend(get_ck_data(soup))

# save to pandas dataframe
df = pd.DataFrame(rtxlist)
print(df)
df.to_csv('casekingRTX.csv')


# acom-pc.de
# RTX 3080

# Asus
url = 'https://www.acom-pc.de/search?page=search&page_action=query&keywords=RTX+3080&sorting=price&desc=on&sdesc=on&acom_search_result_item_count=60&filter_id=21'

soup = getdata(url)
rtxlist = []

rtxlist.extend(get_acomp_data(soup))

# Gigabyte
url = 'https://www.acom-pc.de/search?page=search&page_action=query&keywords=RTX+3080&sorting=price&desc=on&sdesc=on&acom_search_result_item_count=60&filter_id=211'
soup = getdata(url)

rtxlist.extend(get_acomp_data(soup))

# Inno3D
url = 'https://www.acom-pc.de/search?page=search&page_action=query&keywords=RTX+3080&sorting=price&desc=on&sdesc=on&acom_search_result_item_count=60&filter_id=327'
soup = getdata(url)

rtxlist.extend(get_acomp_data(soup))

# MSI
url = 'https://www.acom-pc.de/search?page=search&page_action=query&keywords=RTX+3080&sorting=price&desc=on&sdesc=on&acom_search_result_item_count=60&filter_id=215'
soup = getdata(url)

rtxlist.extend(get_acomp_data(soup))

# Zotac
url = 'https://www.acom-pc.de/search?page=search&page_action=query&keywords=RTX+3080&sorting=price&desc=on&sdesc=on&acom_search_result_item_count=60&filter_id=445'
soup = getdata(url)

rtxlist.extend(get_acomp_data(soup))

# acom-pc.de
# RTX 3070
# ASUS
url = 'https://www.acom-pc.de/search?page=search&page_action=query&keywords=RTX+3070&sorting=price&desc=on&sdesc=on&acom_search_result_item_count=60&filter_id=21'
soup = getdata(url)

rtxlist.extend(get_acomp_data(soup))

# Gigabyte
url = 'https://www.acom-pc.de/search?page=search&page_action=query&keywords=RTX+3070&sorting=price&desc=on&sdesc=on&acom_search_result_item_count=60&filter_id=211'
soup = getdata(url)

rtxlist.extend(get_acomp_data(soup))

# MSI
url = 'https://www.acom-pc.de/search?page=search&page_action=query&keywords=RTX+3070&sorting=price&desc=on&sdesc=on&acom_search_result_item_count=60&filter_id=215'
soup = getdata(url)

rtxlist.extend(get_acomp_data(soup))

# Zotac
url = 'https://www.acom-pc.de/search?page=search&page_action=query&keywords=RTX+3070&sorting=price&desc=on&sdesc=on&acom_search_result_item_count=60&filter_id=445'
soup = getdata(url)

rtxlist.extend(get_acomp_data(soup))

# save to pandas dataframe
df = pd.DataFrame(rtxlist)
print(df)
df.to_csv('acomRTX.csv')
input('Press Enter to exit...')
