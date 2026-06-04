import streamlit as st
import pandas as pd
import yfinance as yf

st.set_page_config(page_title="Nifty 20D Breakout Scanner", layout="wide")
st.title("Nifty 20D Breakout Scanner (Model B)")

symbols = [
    "ADANIENT.NS","ADANIGREEN.NS","ADANIPORTS.NS","ADANIPOWER.NS",
    "AMBUJACEM.NS","APOLLOHOSP.NS","ASIANPAINT.NS","AUROPHARMA.NS",
    "AXISBANK.NS","BAJAJ-AUTO.NS","BAJAJFINSV.NS","BAJFINANCE.NS",
    "BANKBARODA.NS","BEL.NS","BERGEPAINT.NS","BHARATFORG.NS",
    "BHARTIARTL.NS","BHEL.NS","BIOCON.NS","BPCL.NS",
    "BRITANNIA.NS","CANBK.NS","CHOLAFIN.NS","CIPLA.NS",
    "COALINDIA.NS","DABUR.NS","DIVISLAB.NS","DLF.NS",
    "DRREDDY.NS","EICHERMOT.NS","GAIL.NS","GODREJCP.NS",
    "GRASIM.NS","HAL.NS","HAVELLS.NS","HCLTECH.NS",
    "HDFCBANK.NS","HDFCLIFE.NS","HEROMOTOCO.NS","HINDALCO.NS",
    "HINDUNILVR.NS","ICICIBANK.NS","ICICIGI.NS","ICICIPRULI.NS",
    "INDIGO.NS","INDUSINDBK.NS","INFY.NS","IOC.NS",
    "IRCTC.NS","ITC.NS","JINDALSTEL.NS","JIOFIN.NS",
    "JSWENERGY.NS","JSWSTEEL.NS","KOTAKBANK.NS","LICI.NS",
    "LT.NS","LTM.NS","M&M.NS","MARICO.NS",
    "MARUTI.NS","MOTHERSON.NS","NAUKRI.NS","NESTLEIND.NS",
    "NTPC.NS","ONGC.NS","PAGEIND.NS",
    "PIDILITIND.NS","PNB.NS","POWERGRID.NS","RECLTD.NS",
    "RELIANCE.NS","SBICARD.NS","SBILIFE.NS","SBIN.NS",
    "SHREECEM.NS","SHRIRAMFIN.NS","SIEMENS.NS","SUNPHARMA.NS",
    "TATACONSUM.NS","TATAPOWER.NS","TATASTEEL.NS",
    "TCS.NS","TECHM.NS","TITAN.NS","TORNTPHARM.NS",
    "TRENT.NS","TVSMOTOR.NS","ULTRACEMCO.NS","VEDL.NS",
    "WIPRO.NS","ZYDUSLIFE.NS"
]

if st.button("Scan"):
    buy_rows = []
    watchlist_rows = []

    for symbol in symbols:
        try:
            df = yf.download(symbol, period="6mo", auto_adjust=True, progress=False, threads=False)

            if df.empty or len(df) < 50:
                continue

            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)

            high = pd.to_numeric(df["High"], errors="coerce")
            close = pd.to_numeric(df["Close"], errors="coerce")

            current_close = float(close.iloc[-1])
            current_20d_high = float(high.rolling(20).max().shift(1).iloc[-1])

            if pd.isna(current_20d_high):
                continue

            breakout_age = 0
            for i in range(len(df)-2, 19, -1):
                prev20 = high.iloc[i-20:i].max()
                if close.iloc[i] >= prev20:
                    breakout_age += 1
                else:
                    break

            if current_close >= current_20d_high:
                buy_rows.append({
                    "Symbol": symbol.replace(".NS",""),
                    "CMP": round(current_close,2),
                    "20D High": round(current_20d_high,2),
                    "Breakout %": round(((current_close/current_20d_high)-1)*100,2),
                    "Breakout Age": breakout_age
                })
            else:
                gap = ((current_20d_high-current_close)/current_20d_high)*100

                watchlist_rows.append({
                    "Symbol": symbol.replace(".NS",""),
                    "CMP": round(current_close,2),
                    "20D High": round(current_20d_high,2),
                    "Gap %": round(gap,2)
                })

        except Exception:
            pass

    st.subheader(f"🚀 BUY SIGNALS ({len(buy_rows)})")

    if buy_rows:
        buy_df = pd.DataFrame(buy_rows).sort_values(
            ["Breakout Age","Breakout %"],
            ascending=[True,False]
        )
        st.dataframe(buy_df, use_container_width=True, hide_index=True)
    else:
        st.success("No 20D Breakouts Today")

    st.divider()

    st.subheader(f"⏳ WATCHLIST ({len(watchlist_rows)})")

    if watchlist_rows:
        watchlist_df = pd.DataFrame(watchlist_rows).sort_values("Gap %")
        st.dataframe(watchlist_df, use_container_width=True, hide_index=True)
