import os
from scapy.all import *
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import requests
import pandas as pd

# For the capture filter, there is no field in the TCP header for the payload length. There is only a field for the length of the TCP header.
# However, in the IP header, there is a field "total length",
# which includes the length of the IP header and the IP payload (which is the sum of TCP header length and TCP payload length).
# In short "IP total length = IP header length + TCP header length + TCP payload length" which results in:

# TCP payload length = IP total length - IP header length - TCP header leng

# Checks the length of the TCP payload, which is "total length of IP datagram - length of IP header - length of TCP header
# Capturing HTTP traffic for server running on localhost 
# Capturing 10 HTTP requests and writing the output to wire1.pcap file

# Capture Filter used:
## dst port 3000 && ip[2:2] - ((ip[0]&0x0f) << 2) - ((tcp[12]&0xf0) >> 2) > 100
# Server is running on port 3000 and we are capturing HTTP packets only 


######################################################
# /****** Traffic Capture and IP extraction *******\ #
os.system('tshark -f "dst port 3000 && ip[2:2] - ((ip[0]&0x0f) << 2) - ((tcp[12]&0xf0) >> 2) > 100" -c 10 -i lo -w wire1.pcap')

pdcap = rdpcap('wire1.pcap')

#\r\nx-real-ip: 47.9.231.76\r\n\r\n

ip_list = []

for p in pdcap:
    # p[Raw]
    # HTTP Headers are in the Raw sublayer of scapy.layers.l2.ether packet
    raw_l = p[Raw].load.decode('utf-8').split('\r\n')
    ip_list.append(raw_l[-3][11:]) 


######################################################
# /****** Data Processing and Visualization *******\ #

result = []

col_names = ['Continent', 'Country', 'CountryCode', 'Region', 'RegionName', 'City', 'lat', 'lon', 'query']

for query in ip_list:
    try:
        response = requests.get(f'http://ip-api.com/csv/{query[:-1]}?fields=continent,country,countryCode,region,regionName,city,lat,lon,query')
        raw_str = response.content.decode('utf-8')
        raw_lst = raw_str[:len(raw_str)-1].split(',')
        result.append(raw_lst)
    except:
        print('Skipping...')    
#print(result)

ip_info = pd.DataFrame(result, columns = col_names)
ip_info.to_csv('ip.csv')

# read in volcano database data
df = pd.read_csv("ip.csv")

# frequency of Country
freq = df
freq = freq.Country.value_counts().reset_index().rename(columns={"index": "x"})
#print(freq)

# Initialize figure with subplots
fig = make_subplots(
    rows=2, cols=2,
    column_widths=[0.6, 0.4],
    row_heights=[0.4, 0.6],
    specs=[[{"type": "scattergeo", "rowspan": 2}, {"type": "bar"}],
           [            None                    , {"type": "surface"}]])

# Add scattergeo globe map of volcano locations
fig.add_trace(
    go.Scattergeo(lat=df["lat"],
                  lon=df["lon"],
                  mode="markers",
                  hoverinfo="text",
                  showlegend=False,
                  marker=dict(color="crimson", size=4, opacity=0.8)),
    row=1, col=1
)

# Add locations bar chart
fig.add_trace(
    go.Bar(x=freq["x"][0:10],y=freq["Country"][0:10], marker=dict(color="crimson"), showlegend=False),
    row=1, col=2
)

# Update geo subplot properties
fig.update_geos(
    projection_type="orthographic",
    landcolor="white",
    oceancolor="MidnightBlue",
    showocean=True,
    lakecolor="LightBlue"
)

# Rotate x-axis labels
fig.update_xaxes(tickangle=45)

# Set theme, margin, and annotation in layout
fig.update_layout(
    template="plotly_dark",
    margin=dict(r=10, t=25, b=40, l=60),
    annotations=[
        dict(
            text="Server Traffic Visualization",
            showarrow=False,
            xref="paper",
            yref="paper",
            x=0,
            y=0)
    ]
)
print('Data Processing Completed!')
print('You can now Visualize the data in your browser.')
fig.show()