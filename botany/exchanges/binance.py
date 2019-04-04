from urllib.parse import urlencode

import json
import time
import requests

# Bridge to Binance public Rest API
class Binance:

    BASE_URL = "https://www.binance.com/api/v1"
    BASE_V3_URL = "https://www.api.binance.com/api/v3"
    PUBLIC_URL = "https://www.binance.com/exchange/public/product"

    def __init__(self, key, secret):
        self.key = key
        self.secret = secret

    # Test connectivity to the Rest API and return server time.
    def check_connection(self):
        path = "%s/time" % self.BASE_URL
        params = {}
        return self._get(path, params)

    # Current exchange trading rules and symbol info.
    def exchange_info(self):
        path = "%s/exchangeInfo" % self.BASE_URL
        params = {}
        return self._get(path, params)

    # Current average price for a symbol.
    def cur_avg_price(self, symbol):
        path = "%s/avgPrice" % self.BASE_V3_URL
        params = {"symbol": symbol}
        return self._get(path, params)

    # Latest price for a symbol or symbols.
    def get_latest_price(self, symbol):
        path = "%s/ticker/price" % self.BASE_V3_URL
        params = {"symbol": symbol}
        return self._get(path, params)

    # Kline/candlestick bars for a symbol. Klines are uniquely identified by their open time.
    def get_historical_data(self, pairing, candle_interval, limit):
        
        """
        Args:
        pairing (str): Symbol pair to operate on i.e BTCUSDT
        candle_interval (str): Trading time frame i.e 5m or 4h
        limit (int, optional): Number of ticks to return. Default 500; Max 1000 
        
        Returns:
        list: Open time, Open, High, Low, Close, Volume, Close time, Quote asset volume, Number of trades,
            Taker buy base asset volume, Taker buy quote asset volume, Id
        """
        
        if not candle_interval:
            candle_interval = '4h'
        if not limit or limit > 1000:
            limit = 500 

        path = "%s/klines" % self.BASE_URL
        params = {"symbol": pairing,
                  "interval": candle_interval,
                  "limit": limit}
        return self._get(path, params)

    def _get(self, path, params):
        url = "%s?%s" % (path, urlencode(params))
        return requests.get(url, timeout=30, verify=False).json()
