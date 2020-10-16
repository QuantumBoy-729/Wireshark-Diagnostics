import requests, time
from lxml.html import fromstring

proxy_table = {}

def get_proxies():
    url = 'https://free-proxy-list.net/'
    response = requests.get(url)
    parser = fromstring(response.text)
    for i in parser.xpath('//tbody/tr')[:20]:
        if i.xpath('.//td[7][contains(text(),"yes")]'):
            #Grabbing IP and corresponding PORT
            proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
            country = i.xpath('.//td[4]/text()')[0]
            if country not in proxy_table:
                proxy_table[country] = [proxy]
            else:
                proxy_table[country].append(proxy)

get_proxies()
print(proxy_table)    

query = input("Enter the country Name: ")

for proxy in proxy_table[query]:
    print("Trying HTTP proxy %s" % proxy)
    try:
        result = requests.get("http://www.google.com", proxies={'http': proxy})
        print("Got URL using proxy %s" % proxy)
        print(result)
        break
    except:
        print("Trying next proxy in 5 seconds")
        time.sleep(5)
