
import streamlit as st
import pandas as pd
import yfinance as yf
import json
from github import Github

st.set_page_config(page_title="Donchian Reversal Scanner", layout="wide")
st.title("Donchian Reversal Scanner")

# REPLACE WITH YOUR NEW TOKEN
TOKEN = "PASTE_NEW_GITHUB_TOKEN_HERE"
REPO_NAME = "Bishwa2512/20daygtt"
WATCHLIST_FILE = "watchlist.json"

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

def load_watchlist():
    try:
        g = Github(TOKEN)
        repo = g.get_repo(REPO_NAME)
        file = repo.get_contents(WATCHLIST_FILE)
        data = json.loads(file.decoded_content.decode())
        return data.get("watchlist", [])
    except Exception:
        return []

def save_watchlist(watchlist):
    g = Github(TOKEN)
    repo = g.get_repo(REPO_NAME)
    file = repo.get_contents(WATCHLIST_FILE)

    repo.update_file(
        path=WATCHLIST_FILE,
        message="Update Donchian Watchlist",
        content=json.dumps({"watchlist": watchlist}, indent=4),
        sha=file.sha
    )

if "dc_watchlist" not in st.session_state:
    st.session_state.dc_watchlist = load_watchlist()

if st.button("Scan"):

    buy_rows = []
    watchlist_rows = []

    for symbol in symbols:

        try:
            daily = yf.download(
                symbol,
                period="6mo",
                auto_adjust=True,
                progress=False,
                threads=False
            )

            if daily.empty or len(daily) < 50:
                continue

            if isinstance(daily.columns, pd.MultiIndex):
                daily.columns = daily.columns.get_level_values(0)

            high = pd.to_numeric(daily["High"], errors="coerce")
            low = pd.to_numeric(daily["Low"], errors="coerce")
            close = pd.to_numeric(daily["Close"], errors="coerce")

            upper_dc = float(high.rolling(20).max().shift(1).iloc[-1])
            lower_dc = float(low.rolling(20).min().shift(1).iloc[-1])
            latest_close = float(close.iloc[-1])

            ticker = symbol.replace(".NS", "")

            if latest_close < lower_dc:
                if ticker not in st.session_state.dc_watchlist:
                    st.session_state.dc_watchlist.append(ticker)
                    save_watchlist(st.session_state.dc_watchlist)

            if ticker in st.session_state.dc_watchlist and latest_close > upper_dc:

                buy_rows.append({
                    "Symbol": ticker,
                    "CMP": round(latest_close, 2),
                    "Upper DC": round(upper_dc, 2),
                    "Lower DC": round(lower_dc, 2),
                })

                st.session_state.dc_watchlist.remove(ticker)
                save_watchlist(st.session_state.dc_watchlist)

            if ticker in st.session_state.dc_watchlist:

                gap = ((upper_dc - latest_close) / upper_dc) * 100

                watchlist_rows.append({
                    "Symbol": ticker,
                    "CMP": round(latest_close, 2),
                    "Upper DC": round(upper_dc, 2),
                    "Lower DC": round(lower_dc, 2),
                    "Gap %": round(gap, 2)
                })

        except Exception as e:
            st.error(f"{symbol}: {e}")

    st.subheader(f"BUY SIGNALS ({len(buy_rows)})")

    if buy_rows:
        st.dataframe(pd.DataFrame(buy_rows), use_container_width=True, hide_index=True)
    else:
        st.warning("No BUY signals")

    st.divider()

    st.subheader(f"WATCHLIST ({len(watchlist_rows)})")

    if watchlist_rows:
        st.dataframe(
            pd.DataFrame(watchlist_rows).sort_values("Gap %"),
            use_container_width=True,
            hide_index=True
        )

if st.button("Clear GitHub Watchlist"):
    st.session_state.dc_watchlist = []
    save_watchlist([])
    st.success("Watchlist cleared")
