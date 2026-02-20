import datetime as dt
from io import StringIO

import pandas as pd
import requests


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

    period1 = int(start.timestamp())
    period2 = int(end.timestamp())

    url = "https://query1.finance.yahoo.com/v7/finance/download/BTC-USD"
    params = {
        "period1": period1,
        "period2": period2,
        "interval": "1d",
        "events": "history",
        "includeAdjustedClose": "true",
    }

    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()

    csv_text = response.text
    if not csv_text.strip():
        raise ValueError("No data returned from Yahoo Finance for BTC-USD.")

    data = pd.read_csv(StringIO(csv_text), parse_dates=["Date"])
    if data.empty:
        raise ValueError("No data returned from Yahoo Finance for BTC-USD.")

    data = data.set_index("Date")
    data.index.name = "timestamp"

    df = data[["Close"]].rename(columns={"Close": "price"})
    return df

