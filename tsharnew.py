import os
from scapy.all import *
import geoip2.webservice
from ip2geotools.databases.noncommercial import DbIpCity

import csv
import pandas as pd
os.system("tshark -c 10 -f 'dst port 3000'  -i lo -w wire1.pcap")
pdcap=rdpcap('wire1.pcap')
ips=[(p[IP].src,p[IP].dst) for p in pdcap if IP in p]
source=[]
destination=[]
region=[]
country=[]
city=[]
latitude=[]
logitude=[]
status=[]
description=[]
time=[]
source=[]
dest=[]
for i in ips:
    source.append(i[0])
    destination.append(i[1])

for i in source:
    try:
        response = DbIpCity.get(i, api_key='free')
        region.append(response.region)
        country.append(response.country)
        city.append(response.city)
        latitude.append(response.latitude)
        logitude.append(response.longitude)
        k="https://tools.keycdn.com/geo.json?host="+i
        j="curl"+ " " +k+" > curl.txt"
        os.system(j)
        f=open("curl.txt","r")
        a=f.readline()
        c=""
        lis=[]
        for i in a:
            if (i!="{" and i!='"' and i!=','):
                c=c+i
            if (i==":" or i==","):
               lis.append(c)
               c=""
        lis.append(c)
        status.append(lis[1])
        description.append(lis[3])
        time.append(lis[41]+lis[42]+lis[43][0:len(lis[43])-3])
                
        #print(response.to_json())
        
    except (NameError,KeyError,RuntimeError, TypeError):
        region.append("NULL")
        country.append("NULL")
        city.append("NULL")
        latitude.append("NULL")
        logitude.append("NULL")
        status.append("NULL")
        description.append("NULL")
        time.append("NULL")
       # time.append(lis[41]+lis[42]+lis[43][0:len(lis[43])-3])
#print(len(src),len(dest),len(region),len(country),len(city))
with open('innovators1.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["SN","status","description", "src", "dest","region","city","country","latitude","longitude"])
    for i in range(0,len(source)-1):
         writer.writerow([i+1,status[i],description[i], source[i], destination[i],region[i],city[i],country[i],latitude[i],logitude[i]])
         
         
#curl "https://tools.keycdn.com/geo.json?host=www.example.com"
         
