import pandas as pd
import streamlit as st
import requests

st.header('Bitcoin Prices Tracker')

days = st.slider('No of days', 1, 365)
currency = st.radio('Currency', ('CAD', 'USD', 'EUR','INR'))

payload = {'vs_currency': currency, 'days': days, 'interval':'daily'}
api_url ='https://api.coingecko.com/api/v3/coins/bitcoin/market_chart'
req=requests.get(api_url, params=payload)
   
df = None

if req.status_code == 200:
    js_data = req.json()
    data=js_data['prices']
    df=pd.DataFrame(data,columns=['date','prices'])
else:
    print(req.status_code)

df = pd.DataFrame(js_data['prices'], columns=['Date', currency])
df['Date'] = pd.to_datetime(df['Date'], unit='ms')
df = df.set_index('Date')
mean_price = df[currency].mean()

st.line_chart(df[currency])
str_to_display= 'Average price during this time was: {mean_price} in {currency}'
st.write(str_to_display)