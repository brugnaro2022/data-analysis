import datetime
import calendar

# https://api.poloniex.com/markets/BTC_USDT/candles?interval=DAY_1&startTime=1700000000000&endTime=1700600000000
url = "https://api.poloniex.com/markets/BTC_USDT/candles?interval=DAY_1&limit=100"

currencyPair="ETH_USDT"

# unix timestamp: quantidade de segundos desde 1970-01-01 00:00:00 UTC
startTime=1546300800
endTime=1546646400
interval="MINUTE_15"  # period -> HOUR_4, DAY_1

initialDate = datetime.datetime.utcfromtimestamp(startTime).strftime("%d-%m-%Y")
finalDate = datetime.datetime.utcfromtimestamp(endTime).strftime("%d-%m-%Y")

# convertendo para timestamp (caminho inverso)
i_date = "01-01-2019"
f_date = "05-01-2019"

initial_date = datetime.datetime.strptime(i_date, "%d-%m-%Y")
initial_date_separated = initial_date.timetuple()
initial_date_timestamp = calendar.timegm(initial_date_separated)

final_date = datetime.datetime.strptime(f_date, "%d-%m-%Y")
final_date_separated = final_date.timetuple()
final_date_timestamp = calendar.timegm(final_date_separated)

print(initial_date_timestamp)
print(final_date_timestamp)
