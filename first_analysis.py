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

# client = SpotRestClient(api_key=api_key, api_secret=secret_key)

client = MagicMock()
client.orders().create.return_value = {'id': '111', 'clientOrderId': ''}

mock_balances = {'USDT': 1000.0, 'ETH': 2.3, 'BTC': 0.5, 'ANDYETH': 1.3}

def get_balance(currency):
  return mock_balances.get(currency, 0.0)

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

# plt.ion()


def get_quotes(currency):
  final_timestamp = (int(datetime.datetime.utcnow().timestamp())) + 3 * 60 *60

  past_seconds = 48 * 60 * 60 # Quantidade de segundos existentes em 48hs

  initial_timestamp = final_timestamp - past_seconds 

  url = "https://api.poloniex.com/markets/"+ currency + "/candles?interval=MINUTE_15&startTime=" + str(initial_timestamp * 1000) + "&endTime=" + str(final_timestamp * 1000)

  req = requests.get(url)
  data = json.loads(req.text)

  return data

def make_purchase(value, currency):
  base = currency.split('_')[0]
  balance = get_balance('USDT')

  if balance < value:
    return -1

  price = get_purchase_price(currency)
  eth_bought = value / price
  mock_balances['USDT'] -= value
  mock_balances[base] = mock_balances.get(base, 0.0) + eth_bought

  print(f'{base} comprado: {eth_bought:.4f}')

  res = client.orders().create(side='BUY', amount=str(value), symbol=currency)
  return res['id'] if 'id' in res else -2

def make_sale(quantity, currency):
  base = currency.split('_')[0]
  balance = get_balance(base)

  if balance < quantity:
    return -1

  price = get_sale_price(currency)
  usdt_received = quantity * price
  mock_balances[base] -= quantity
  mock_balances['USDT'] = mock_balances.get('USDT', 0.0) + usdt_received

  print(f'{base} vendido: {quantity:.4f} a {price} = {usdt_received:.2f} USDT')

  res = client.orders().create(side='SELL', quantity=str(quantity), symbol=currency)
  return res['id'] if 'id' in res else -2

# print('Saldo inicial')
# print('USDT:', get_balance('USDT'))
# print('ETH:', get_balance('ETH'))
# print('Preço ETH_USDT:', get_purchase_price('ETH_USDT'))

# print(10*'-')
# print('Compra 10 ETH_USDT')
# print(make_purchase(10, 'ETH_USDT'))

# print(10*'-')
# print('Saldo atualizado')
# print('USDT:', get_balance('USDT'))
# print('ETH:', get_balance('ETH'))
# print('Preço ETH_USDT:', get_purchase_price('ETH_USDT'))

# print(10*'-')
# print('Venda 0.001 ETH_USDT')
# print(make_sale(0.001, 'ETH_USDT'))

# print(10*'-')
# print('Saldo após venda')
# print('USDT:', get_balance('USDT'))
# print('ETH:', get_balance('ETH'))
# print('Preço ETH_USDT:', get_sale_price('ETH_USDT'))

# input()




# req = requests.get('https://api.poloniex.com/markets/ticker24h')
# tickers = json.loads(req.text)

# tickers_usdt = [t for t in tickers if t['symbol'].endswith('_USDT')]
# tickers_sorted = sorted(tickers_usdt, key=lambda x: abs(float(x['dailyChange'])), reverse=True)

# for t in tickers_sorted[:10]:
#     print(f"{t['symbol']}: {float(t['dailyChange'])*100:.2f}%")

# input()



# ANDYETH_USDT: 23978.57%
# SACHI_USDT: 3117.16%
# UXLINK_USDT: 1587.34%
# BNKR_USDT: 1582.65%
# POD_USDT: 1106.84%
# BOSS_USDT: 609.09%
# MRDN_USDT: 352.83%
# COPPERINU_USDT: 184.85%
# MANYUETH_USDT: 182.71%
# PENG_USDT: 159.80%



AWAITING_PURCHASE_SIGNAL = 0
AWAITING_SELL_SIGNAL = 1
STATE = AWAITING_PURCHASE_SIGNAL

CURRENCY = "ETH_USDT"
OPERATION_VALUE = 10

PURCHASE_VALUE = 0
PURCHASE_SELL = 0
PROFITABILITY = 0

WORK_MODE = "V"

THRESHOLD = 0.0025

while True:
  data = get_quotes(CURRENCY)

  quotes = []
  for e in data:
    quotes.append(float(e[3]))
  
  fast_mean = [sum(quotes[-8:]) / 8] * len(quotes)
  slow_mean = [sum(quotes[-21:]) / 21] * len(quotes)

  if STATE == AWAITING_PURCHASE_SIGNAL:
    print(f'[SINAL] Aguardando compra | fast: {fast_mean[0]:.2f} | slow: {slow_mean[0]:.2f} | threshold: {slow_mean[0] + (slow_mean[0] * THRESHOLD):.2f}')
    if fast_mean[0] > slow_mean[0] + (slow_mean[0] * THRESHOLD):
      if WORK_MODE == "R":
        print('[COMPRA REAL] Sinal de compra detectado!')
        make_purchase(OPERATION_VALUE, CURRENCY)
      elif WORK_MODE == "V":
        PURCHASE_VALUE = get_purchase_price(CURRENCY)
        print('Valor da compra: ' + str(PURCHASE_VALUE))

      STATE = AWAITING_SELL_SIGNAL


  elif STATE == AWAITING_SELL_SIGNAL:
    print(f'[SINAL] Aguardando venda | fast: {fast_mean[0]:.2f} | slow: {slow_mean[0]:.2f} | threshold: {slow_mean[0] - (slow_mean[0] * THRESHOLD):.2f}')
    if fast_mean[0] < slow_mean[0] - (slow_mean[0] * THRESHOLD):
      if WORK_MODE == "R":
        print('[VENDA] Sinal de venda detectado!')
        make_sale(OPERATION_VALUE, CURRENCY)
      elif WORK_MODE == "V":
        PURCHASE_SELL = get_sale_price(CURRENCY)
        print('Valor da venda: ' + str(PURCHASE_SELL))

        # PROFITABILITY = PROFITABILITY + ((PURCHASE_SELL - PURCHASE_VALUE) / PURCHASE_VALUE) * 100
        PROFITABILITY = PROFITABILITY + (((PURCHASE_SELL * 100) / PURCHASE_VALUE) - 100)
        print('Rentabilidade: ' + str(PROFITABILITY) + '%')
      
      STATE = AWAITING_PURCHASE_SIGNAL



  # ga = plt.gca()
  # ga.clear()
  
  # plt.plot(quotes[-50:])
  # plt.xticks(range(0, len(quotes) + 1, 20))
  # plt.title(f"Última cotação: {quotes[-1]}")
  # plt.plot(fast_mean[-50:], color='red')
  # plt.plot(slow_mean[-50:], color='green')
  # plt.draw()
  # plt.pause(5)

  time.sleep(2)
