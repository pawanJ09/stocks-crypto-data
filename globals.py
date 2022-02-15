headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                         "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.3 Safari/605.1.15"}
url = 'https://query1.finance.yahoo.com/v7/finance/download/{0}?' \
      'period1={1}&period2={2}&interval=1d&events=history&includeAdjustedClose=true'
entity_dict = {"Bitcoin": "BTC-USD", "Dogecoin": "DOGE-USD", "Shibainu": "SHIB-USD",
               "Ethereum": "ETH-USD", "Accenture": "ACN", "Apple": "AAPL", "Google": "GOOG"}
