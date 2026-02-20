import datetime as dt

import pandas as pd
import yfinance as yf


def fetch_bitcoin_market_chart(vs_currency: str = "usd", days: int = 30) -> pd.DataFrame:
    """
    Fetch recent Bitcoin market data from Yahoo Finance (BTC-USD).

    Parameters
    ----------
    vs_currency : str, optional
        Quote currency (e.g. "usd", "eur"), by default "usd".
    days : int, optional
        Number of past days of data to retrieve. By default 30.

    Returns
    -------
    pandas.DataFrame
        DataFrame indexed by timestamp with columns:
        - "price": Bitcoin price in the requested quote currency.
    """
    if vs_currency.lower() != "usd":
        raise ValueError("Yahoo Finance BTC-USD only supports USD as quote currency.")

    end = dt.datetime.utcnow()
    start = end - dt.timedelta(days=days)

    ticker = yf.Ticker("BTC-USD")
    data = ticker.history(start=start, end=end, interval="1d")

    if data.empty:
        raise ValueError("No data returned from Yahoo Finance for BTC-USD.")

    df = data[["Close"]].rename(columns={"Close": "price"})
    df.index.name = "timestamp"

    return df

