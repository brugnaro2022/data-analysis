import datetime
import calendar
import requests
import json
import matplotlib.pyplot as plt
from polosdk import SpotRestClient
import time
import urllib.parse
import hmac
import hashlib
from config import api_key, secret_key
from unittest.mock import MagicMock

api_key = api_key
secret_key = secret_key

client_ = SpotRestClient(api_key=api_key, api_secret=secret_key)

client = MagicMock()
client.accounts().get_balances.return_value = [
    {
        'accountId': '392487043327959040',
        'accountType': 'SPOT',
        'balances': [
            {'currency': 'BTC', 'available': '0.5', 'hold': '0'},
            {'currency': 'USDT', 'available': '1000.0', 'hold': '0'},
            {'currency': 'ETH', 'available': '2.3', 'hold': '0'},
        ]
    }
]

def get_balance(currency):
  try:
    balances = client.accounts().get_balances(account_type='SPOT')
    # print(client.accounts())
    for account in balances:
      for b in account['balances']:
        if b['currency'] == currency:
          return float(b['available'])
    return None
  except Exception as e:
    # print(e)
    return None

  # try:
  #   params = {'command': 'returnBalances', 'nonce': int(time.time()*1000)}
  #   params_encoded = urllib.parse.urlencode(params).encode('utf8')
  #   params_signed = hmac.new(secret_key, params_encoded, hashlib.sha512).hexdigest()

  #   headers = {'Key': api_key, 'Sign': params_signed}

  #   req = requests.post('https://poloniex.com/tradingApi', headers=headers, data=params)

  #   res = json.loads(req.text)

  #   return float(res[currency])
  # except:
  #   return None

# print(get_balance('BTC'))
# print(get_balance('USDT'))

def get_purchase_price(currency):
  url_ticker = 'https://api.poloniex.com/markets/' + currency + '/ticker24h'
  req = requests.get(url_ticker)
  res = json.loads(req.text)
  last_price = float(res['ask'])
  return last_price

def get_sale_price(currency):
  url_ticker = 'https://api.poloniex.com/markets/' + currency + '/ticker24h'
  req = requests.get(url_ticker)
  res = json.loads(req.text)
  last_price = float(res['bid'])
  return last_price


# date_to_timestamp = lambda x: calendar.timegm((datetime.datetime.strptime(x, "%d-%m-%Y")).timetuple())
# timestamp_to_date = lambda x: datetime.datetime.utcfromtimestamp(x).strftime("%d-%m-%Y")

# currencyPair="ETH_USDT"

# unix timestamp: quantidade de segundos desde 1970-01-01 00:00:00 UTC
# startTime=1546300800
# endTime=1546646400
# interval="MINUTE_15"  # period -> HOUR_4, DAY_1

# initialDate = datetime.datetime.utcfromtimestamp(startTime).strftime("%d-%m-%Y")
# finalDate = datetime.datetime.utcfromtimestamp(endTime).strftime("%d-%m-%Y")

# convertendo para timestamp (caminho inverso)
# i_date = "01-01-2019"
# f_date = "05-01-2019"

# initial_date = datetime.datetime.strptime(i_date, "%d-%m-%Y")
# initial_date_separated = initial_date.timetuple()
# initial_date_timestamp = calendar.timegm(initial_date_separated)

# final_date = datetime.datetime.strptime(f_date, "%d-%m-%Y")
# final_date_separated = final_date.timetuple()
# final_date_timestamp = calendar.timegm(final_date_separated)

# print(initial_date_timestamp)
# print(final_date_timestamp)

# print(date("01-01-2019"))
# print(date("05-01-2019"))

'''
    Índice	Valor	Descrição
    0	146.26	low — menor preço no período
    1	147.19	high — maior preço no período
    2	147.19	open — preço de abertura
    3	146.35	close — preço de fechamento
    4	19076.27	amount — volume em moeda cotada (USDT)
    5	130.002762	quantity — volume em moeda base (ETH)
    6	0	buyTakerAmount — volume comprado por takers em USDT
    7	0	buyTakerQuantity — volume comprado por takers em ETH
    8	0	tradeCount — número de trades no período
    9	1546557300000	ts — timestamp de criação do candle (ms)
    10	146.73	weightedAverage — preço médio ponderado pelo volume
    11	MINUTE_15	interval — intervalo do candle
    12	1546557300000	startTime — início do período (ms)
    13	1546558199999	closeTime — fim do período (ms)
    Os valores 6 e 7 estão zerados pois a API pode não ter retornado dados de taker para esse período histórico.
'''

# initial_date = date_to_timestamp("15-07-2020")
# final_date = int(datetime.datetime.utcnow().timestamp())
# final_date = date_to_timestamp("16-07-2020")

# initial_date = date_to_timestamp("03-05-2026")
# final_date = int(datetime.datetime.utcnow().timestamp())

plt.ion()


def get_quotes(currency):
  final_timestamp = (int(datetime.datetime.utcnow().timestamp())) + 3 * 60 *60

  past_seconds = 48 * 60 * 60 # Quantidade de segundos existentes em 48hs

  initial_timestamp = final_timestamp - past_seconds 

  url = "https://api.poloniex.com/markets/"+ currency + "/candles?interval=MINUTE_15&startTime=" + str(initial_timestamp * 1000) + "&endTime=" + str(final_timestamp * 1000)

  req = requests.get(url)
  data = json.loads(req.text)

  return data

while True:
  data = get_quotes("ETH_USDT")
  quotes = []
  for e in data:
    quotes.append(float(e[3]))
  
  fast_mean = [sum(quotes[-8:]) / 8] * len(quotes)
  slow_mean = [sum(quotes[-21:]) / 21] * len(quotes)
  
  ga = plt.gca()
  ga.clear()
  
  plt.plot(quotes[-50:])
  plt.xticks(range(0, len(quotes) + 1, 20))
  plt.title(f"Última cotação: {quotes[-1]}")
  plt.plot(fast_mean[-50:], color='red')
  plt.plot(slow_mean[-50:], color='green')
  plt.draw()
  plt.pause(5)

