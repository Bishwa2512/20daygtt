import streamlit as st
import pandas as pd
import yfinance as yf

st.set_page_config(page_title='20D Breakout Scanner', layout='wide')
st.title('Nifty 20D High GTT Scanner')

symbols=['INFY.NS','TCS.NS','HCLTECH.NS','WIPRO.NS','RELIANCE.NS','ICICIBANK.NS','HDFCBANK.NS','SBIN.NS']

if st.button('Scan'):
    rows=[]
    for s in symbols:
        try:
            df=yf.download(s,period='6mo',auto_adjust=True,progress=False,threads=False)
            if isinstance(df.columns,pd.MultiIndex):
                df.columns=df.columns.get_level_values(0)
            if len(df)<25:
                continue
            close=float(df['Close'].iloc[-1])
            high20=float(df['High'].rolling(20).max().shift(1).iloc[-1])
            if close<=high20:
                rows.append({'Symbol':s,'CMP':round(close,2),'20D High':round(high20,2),'GTT':round(high20,2)})
        except:
            pass
    st.dataframe(pd.DataFrame(rows),use_container_width=True)
