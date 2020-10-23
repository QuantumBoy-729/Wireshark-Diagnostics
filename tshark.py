import os
import geoip2.webservice
from ip2geotools.databases.noncommercial import DbIpCity
from scapy.all import *
import csv
import pandas as pd
#reader = geoip2.database.Reader(‘./GeoLite2-City_20190115/GeoLite2-City.mmdb’)
os.system("tshark -c 300 >tshark.txt")



f=open("tshark.txt","r")
b=[]
c=[]
src=[]
dest=[]
port=[]
region=[]
country=[]
city=[]
latitude=[]
logitude=[]
#response.latitude
#response.longitude
for x in f:
    b.append(x)
for i in range(0,len(b)):
    c.append(b[i].split(' '))
#for i in range(0,len(c)-1):
b=c[9][6]

for i in c:
    for j in range(0,len(i)-1):
        if (i[j]==b):
            src.append(i[j-1])
            dest.append(i[j+1])
            break

for i in dest:
    try:
        response = DbIpCity.get(i, api_key='free')
        region.append(response.region)
        country.append(response.country)
        city.append(response.city)
        latitude.append(response.latitude)
        logitude.append(response.longitude)
        #print(response.to_json())
        
    except (NameError,KeyError,RuntimeError, TypeError):
        region.append("Location not found")
        country.append("Location not found")
        city.append("Location not found")
        latitude.append("Location not found")
        logitude.append("Location not found")
#print(len(src),len(dest),len(region),len(country),len(city))
with open('innovators.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["SN", "src", "dest","region","country","latitude","longitude"])
    for i in range(0,len(src)):
         writer.writerow([i, src[i], dest[i],region[i],country[i],latitude[i],logitude[i]])
         
