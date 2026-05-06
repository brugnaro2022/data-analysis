import datetime
import calendar
import requests
import json
import matplotlib.pyplot as plt

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

while True:
  # final_date = datetime.datetime.now()
  # final_timestamp = calendar.timegm(final_date.timetuple())
  final_timestamp = int(datetime.datetime.utcnow().timestamp())

  past_seconds = 48 * 60 * 60 # Quantidade de segundos existentes em 48hs

  initial_timestamp = final_timestamp - past_seconds 

  # print(timestamp_to_date(initial_timestamp))
  # print(timestamp_to_date(final_timestamp))
  # input() 

  url = "https://api.poloniex.com/markets/ETH_USDT/candles?interval=MINUTE_15&startTime=" + str(initial_timestamp * 1000) + "&endTime=" + str(final_timestamp * 1000)

  req = requests.get(url)
  data = json.loads(req.text)

  quotes = []
  for e in data:
    quotes.append(float(e[3]))

  # print(quotes)
  # input()

  print(quotes[-1:])
  # input()

  ga = plt.gca()
  ga.clear()
  
  plt.plot(quotes)
  plt.xticks(range(0, len(quotes) + 1, 20))
  plt.title(f"Última cotação: {quotes[-1]}")
  plt.draw()
  plt.pause(5)

