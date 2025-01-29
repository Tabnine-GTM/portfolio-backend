import requests
from app.config import settings


from typing import Any, Dict


def fetch_daily_stock_data(symbol: str) -> Dict[str, Dict[str, str]]:
    api_key = settings.ALPHA_VANTAGE_API_KEY
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}"

    response = requests.get(url)
    data = response.json()

    if "Time Series (Daily)" not in data:
        raise ValueError("Unable to fetch stock data from Alpha Vantage API")

    return data["Time Series (Daily)"]


def fetch_stock_overview(symbol: str) -> Dict[str, Any]:
    api_key = settings.ALPHA_VANTAGE_API_KEY
    url = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey={api_key}"

    response = requests.get(url)
    data = response.json()

    return data


def fetch_multiple_stock_data(symbols: list[str]) -> Dict[str, Dict[str, str]]:
    api_key = settings.ALPHA_VANTAGE_API_KEY
    symbols_str = ",".join(symbols)
    url = f"https://www.alphavantage.co/query?function=BATCH_STOCK_QUOTES&symbols={symbols_str}&apikey={api_key}"

    response = requests.get(url)
    data = response.json()

    if "Stock Quotes" not in data:
        raise ValueError("Unable to fetch stock data from Alpha Vantage API")

    result = {}
    for quote in data["Stock Quotes"]:
        symbol = quote["1. symbol"]
        result[symbol] = {
            "price": quote["2. price"],
            "volume": quote["3. volume"],
            "timestamp": quote["4. timestamp"],
        }

    return result
