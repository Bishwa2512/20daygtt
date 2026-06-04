import streamlit as st
import pandas as pd
import yfinance as yf

st.set_page_config(
    page_title="20 Day Breakout Scanner",
    layout="wide"
)

st.title("20 Day Breakout Scanner")

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

    rows = []
    buy_rows = []

    progress = st.progress(0)
    status = st.empty()

    for idx, symbol in enumerate(symbols):

        status.write(f"Scanning {symbol}...")

        try:

            df = yf.download(
                symbol,
                period="6mo",
                auto_adjust=True,
                progress=False,
                threads=False
            )

            if df.empty or len(df) < 50:
                continue

            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)

            high = df["High"].astype(float)
            close = df["Close"].astype(float)

            # ----- BUY SIGNAL CHECK -----
            current_close = float(close.iloc[-1])

            current_20d_high = float(
                high.rolling(20).max().shift(1).iloc[-1]
            )

            if pd.isna(current_20d_high):
                continue

            if current_close >= current_20d_high:

                buy_rows.append({
                    "Symbol": symbol.replace(".NS", ""),
                    "CMP": round(current_close, 2),
                    "20D High": round(current_20d_high, 2)
                })

            # ----- EXISTING WATCHLIST LOGIC -----

            breakout_found = False

            for i in range(len(df) - 20, len(df)):

                if i < 20:
                    continue

                prev20_high = high.iloc[i-20:i].max()
                current_high = high.iloc[i]

                if current_high > prev20_high:
                    breakout_found = True
                    break

            if breakout_found:
                continue

            if current_close > current_20d_high:
                continue

            rows.append({
                "Symbol": symbol.replace(".NS", ""),
                "CMP": round(current_close, 2),
                "20D High": round(current_20d_high, 2),
                "GTT Price": round(current_20d_high, 2)
            })

        except:
            pass

        progress.progress((idx + 1) / len(symbols))

    status.empty()

    buy_df = pd.DataFrame(buy_rows)

    if not buy_df.empty:

        st.error(
            f"🚀 BUY SIGNALS TODAY ({len(buy_df)})"
        )

        st.dataframe(
            buy_df.sort_values("Symbol"),
            use_container_width=True,
            hide_index=True
        )

    else:

        st.success("No Buy Signals Today")

    st.markdown("---")

    result = pd.DataFrame(rows)

    if result.empty:

        st.warning("No stocks found")

    else:

        result = result.sort_values("Symbol")

        st.subheader(
            f"Watchlist ({len(result)} Stocks)"
        )

        st.dataframe(
            result,
            use_container_width=True,
            hide_index=True
        )

        csv = result.to_csv(index=False).encode("utf-8")

        st.download_button(
            "Download Watchlist CSV",
            csv,
            file_name="watchlist.csv",
            mime="text/csv"
        )
