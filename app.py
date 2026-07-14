
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
   "IDEA.NS",
"IFCI.NS",
"OLAELEC.NS",
"YESBANK.NS",
"GTLINFRA.NS",
"MOTISONS.NS",
"GROWW.NS",
"JPPOWER.NS",
"SUZLON.NS",
"TATSILV.NS",
"PCJEWELLER.NS",
"ASHOKLEY.NS",
"RENUKA.NS",
"NHPC.NS",
"HCC.NS",
"SEPC.NS",
"ZEEL.NS",
"ETERNAL.NS",
"HDFCBANK.NS",
"KALYANKJIL.NS",
"ASHOKA.NS",
"AEQUS.NS",
"KWIL.NS",
"MAHABANK.NS",
"RPOWER.NS",
"EXICOM.NS",
"PINELABS.NS",
"NMDC.NS",
"IDFCFIRSTB.NS",
"VEDL.NS",
"APOLLO.NS",
"MMTC.NS",
"MEESHO.NS",
"TATASTEEL.NS",
"ADANIPOWER.NS",
"CENTRALBK.NS",
"SOUTHBANK.NS",
"EASEMYTRIP.NS",
"ONGC.NS",
"TMCV.NS",
"GMRAIRPORT.NS",
"MOREPENLAB.NS",
"IOC.NS",
"SWIGGY.NS",
"MOTHERSON.NS",
"NBCC.NS",
"BHARATCOAL.NS",
"RHETAN.NS",
"BAJAJHIND.NS",
"IDBI.NS",
"CANBK.NS",
"SAGILITY.NS",
"INOXWIND.NS",
"MCLOUD.NS",
"AURIGROW.NS",
"PNB.NS",
"RELIANCE.NS",
"DEN.NS",
"CUPID.NS",
"GAIL.NS",
"RTNPOWER.NS",
"AARTIIND.NS",
"JIOFIN.NS",
"ALOKINDS.NS",
"NTPC.NS",
"FCL.NS",
"SCI.NS",
"MSUMI.NS",
"ICICIBANK.NS",
"SAIL.NS",
"BPCL.NS",
"ANGELONE.NS",
"MRPL.NS",
"KOTAKBANK.NS",
"CCAVENUE.NS",
"WIPRO.NS",
"LTF.NS",
"BANDHANBNK.NS",
"RAMASTEEL.NS",
"HSCL.NS",
"FIVESTAR.NS",
"AQYLON.NS",
"IRB.NS",
"SBIN.NS",
"SAMMAANCAP.NS",
"SHRIRAMFIN.NS",
"BAJFINANCE.NS",
"RAIN.NS",
"JYOTISTRUC.NS",
"BEL.NS",
"DIACABS.NS",
"UJJIVANSFB.NS",
"ITC.NS",
"TMPV.NS",
"SBC.NS",
"IRFC.NS",
"BCG.NS",
"STEELXIND.NS",
"ATALREAL.NS",
"DAVANGERE.NS",
"NETWORK18.NS",
"AHCL.NS",
"COALINDIA.NS",
"HINDPETRO.NS",
"BANKBARODA.NS",
"POWERGRID.NS",
"DLF.NS",
"ELECTCAST.NS",
"NATIONALUM.NS",
"RVNL.NS",
"TATAPOWER.NS",
"AEGISLOG.NS",
"AIIL.NS",
"HINDALCO.NS",
"FEDERALBNK.NS",
"UNIONBANK.NS",
"RBLBANK.NS",
"NLCINDIA.NS",
"LEMONTREE.NS",
"EQUITASBNK.NS",
"PAISALO.NS",
"VMM.NS",
"HATHWAY.NS",
"INFY.NS",
"BHEL.NS",
"HFCL.NS",
"TRIDENT.NS",
"VBL.NS",
"BANKINDIA.NS",
"AXISBANK.NS",
"EPACKPEB.NS",
"MANINFRA.NS",
"SHAH.NS",
"ASIANTILES.NS",
"MSTCLTD.NS",
"PARAS.NS",
"BELRISE.NS",
"UTKARSHBNK.NS",
"CMRGREEN.NS",
"INDUSTOWER.NS",
"SALASAR.NS",
"LENSKART.NS",
"TEJASNET.NS",
"IREDA.NS",
"J&KBANK.NS",
"ARFIN.NS",
"PPLPHARMA.NS",
"MSPL.NS",
"ALLCARGO.NS",
"TTML.NS",
"BAJAJHFL.NS",
"PFC.NS",
"CGCL.NS",
"NYKAA.NS",
"RTNINDIA.NS",
"PWL.NS",
"ITCHOTELS.NS",
"HDBFS.NS",
"EDELWEISS.NS",
"UCOBANK.NS",
"UNITECH.NS",
"NSLNISP.NS",
"AEROFLEX.NS",
"BHARTIARTL.NS",
"MONIFTY500.NS",
"M&M.NS",
"HINDZINC.NS",
"LLOYDSENGG.NS",
"SPAL.NS",
"OIL.NS",
"KELLTONTEC.NS",
"PETRONET.NS",
"JAINREC.NS",
"RUSHIL.NS",
"M&MFIN.NS",
"BSE.NS",
"TATACAP.NS",
"CUB.NS",
"IEX.NS",
"HINDCOPPER.NS",
"SUMEETINDS.NS",
"GATECH.NS",
"JSWINFRA.NS",
"PATELENG.NS",
"GRMOVER.NS",
"AWL.NS",
"CHOLAFIN.NS",
"TFCILTD.NS",
"AJMERA.NS",
"E2E.NS",
"CMPDI.NS",
"CASTROLIND.NS",
"IGL.NS",
"ABCAPITAL.NS",
"CAMLINFINE.NS",
"EXXARO.NS",
"IXIGO.NS",
"SPARC.NS",
"REDINGTON.NS",
"LT.NS",
"EMBDL.NS",
"MCX.NS",
"RECLTD.NS",
"JMFINANCIL.NS",
"KAMDHENU.NS",
"YATRA.NS",
"TIMETECHNO.NS",
"JAYNECOIND.NS",
"QUADFUTURE.NS",
"VINCOFE.NS",
"DELHIVERY.NS",
"EXIDEIND.NS",
"JTLIND.NS",
"URBANCO.NS",
"ABFRL.NS",
"RBA.NS",
"AGIIL.NS",
"GREENPOWER.NS",
"ABINFRA.NS",
"IOB.NS",
"EMMVEE.NS",
"TPHQ.NS",
"NTPCGREEN.NS",
"HINDWAREAP.NS",
"TCS.NS",
"AMBUJACEM.NS",
"VIKRAMSOLR.NS",
"MSCIINDIA.NS",
"HUDCO.NS",
"BIOCON.NS",
"AUROPHARMA.NS",
"JAYBARMARU.NS",
"PCBL.NS",
"MTARTECH.NS",
"WAKEFIT.NS",
"LLOYDSENT.NS",
"INDUSINDBK.NS",
"KTKBANK.NS",
"MOSMALL250.NS",
"VIKASLIFE.NS",
"CROMPTON.NS",
"IOLCP.NS",
"MOBIKWIK.NS",
"PGEL.NS",
"JSWCEMENT.NS",
"LICI.NS",
"WELSPUNLIV.NS",
"JSWENERGY.NS",
"JISLJALEQS.NS",
"CDSL.NS"
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


# ==========================================================
# GOOGLE SHEET FINAL LIST (Independent of Donchian Scanner)
# ==========================================================

import requests

st.divider()
st.header("📋 Final List")

# Replace with your Final List tab gid
FINAL_LIST_GID = "YOUR_GID_HERE"

CSV_URL = "https://docs.google.com/spreadsheets/d/1wopIdWgQMfBIJ9DnKcGDVmdDM2JiV06HgZLEkNUZaKk/export?format=csv&gid=1924424194"

STATUS_FILE = "status_history.json"


def load_status_history():
    try:
        g = Github(TOKEN)
        repo = g.get_repo(REPO_NAME)
        file = repo.get_contents(STATUS_FILE)
        return json.loads(file.decoded_content.decode())
    except:
        return {}


def save_status_history(data):
    g = Github(TOKEN)
    repo = g.get_repo(REPO_NAME)

    content = json.dumps(data, indent=4)

    try:
        file = repo.get_contents(STATUS_FILE)
        repo.update_file(
            STATUS_FILE,
            "Update Status History",
            content,
            file.sha,
        )
    except:
        repo.create_file(
            STATUS_FILE,
            "Create Status History",
            content,
        )


try:
    sheet = pd.read_csv(CSV_URL)

    history = load_status_history()

    for _, row in sheet.iterrows():

        symbol = str(row["Symbol"]).strip()
        status = str(row["Status"]).strip().upper()

        if symbol not in history:
            history[symbol] = {
                "status": status,
                "changed_on": pd.Timestamp.now().strftime("%d-%b-%Y %H:%M")
            }

        elif history[symbol]["status"] != status:
            history[symbol]["status"] = status
            history[symbol]["changed_on"] = pd.Timestamp.now().strftime("%d-%b-%Y %H:%M")

    save_status_history(history)

    sheet["Status Changed On"] = sheet["Symbol"].map(
        lambda x: history.get(str(x), {}).get("changed_on", "")
    )

    st.dataframe(
        sheet,
        use_container_width=True,
        hide_index=True
    )

except Exception as e:
    st.error(f"Unable to load Final List: {e}")
