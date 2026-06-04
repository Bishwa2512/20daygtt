import pandas as pd
import yfinance as yf

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

rows = []
buy_signals = []

for symbol in symbols:

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

        # Existing logic
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

        current_close = float(close.iloc[-1])

        current_20d_high = float(
            high.rolling(20).max().shift(1).iloc[-1]
        )

        if pd.isna(current_20d_high):
            continue

        buy_signal = ""

        if current_close >= current_20d_high:
            buy_signal = "BUY"
            buy_signals.append(symbol)

        rows.append({
            "Symbol": symbol.replace(".NS", ""),
            "CMP": round(current_close, 2),
            "20D High": round(current_20d_high, 2),
            "GTT Price": round(current_20d_high, 2),
            "BUY SIGNAL": buy_signal
        })

    except Exception as e:
        print(f"{symbol}: {e}")

result = pd.DataFrame(rows)

print("\n" + "=" * 100)
print("BUY SIGNALS TODAY")
print("=" * 100)

if buy_signals:
    for s in buy_signals:
        print(s)
else:
    print("No Buy Signals")

print("\n" + "=" * 100)
print("WATCHLIST")
print("=" * 100)

if result.empty:
    print("No stocks found")
else:
    result = result.sort_values("Symbol")
    print(result.to_string(index=False))
    print(f"\nTotal Stocks: {len(result)}")
