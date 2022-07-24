import csv
from matplotlib import pyplot as plt
from datetime import datetime

###############################################
# filename = "sitka_weather_07-2014.csv"
# with open(filename) as f:
#     reader = csv.reader(f)
#     header_row = next(reader)
#
#     # for index, column_header in enumerate(header_row):
#     #     print(index, column_header)
#
#     dates, highs = [], []
#
#     for row in reader:
#         current_date = datetime.strptime(row[0].replace('/', '-'), '%Y-%m-%d')
#         dates.append(current_date)
#         highs.append(int(row[1]))
#     print(highs)
#     print(dates)
#
#     fig = plt.figure(dpi=128, figsize=(10, 6))
#     plt.plot(dates, highs, c='red')
#
#     # 设置图形的格式
#     plt.title("Display high temperatures, July 2014", fontsize=24)
#     plt.xlabel('', fontsize=16)
#     fig.autofmt_xdate()
#     plt.ylabel("Temperature (F)", fontsize=16)
#     plt.tick_params(axis='both', which='major', labelsize=16)
#
#     plt.show()


######################################
# 换个数据集 sitka_weather_2014.csv, 同时再添加最低气温
# filename = "sitka_weather_2014.csv"
# with open(filename) as f:
#     reader = csv.reader(f)
#     header_row = next(reader)
#
#     dates, highs, lows = [], [], []
#
#     for row in reader:
#         current_date = datetime.strptime(row[0].replace('/', '-'), '%Y-%m-%d')
#         high = int(row[1])
#         low = int(row[3])
#         dates.append(current_date)
#         highs.append(high)
#         lows.append(low)
#
#     fig = plt.figure(dpi=128, figsize=(10, 6))
#     plt.plot(dates, highs, c='red', alpha=0.5)
#     plt.plot(dates, lows, c='blue', alpha=0.5)
#     plt.fill_between(dates, highs, lows, facecolor='blue', alpha=0.1)
#
#     # 设置图形的格式
#     plt.title("Daily high and low temperatures - 2014", fontsize=24)
#     plt.xlabel('', fontsize=16)
#     fig.autofmt_xdate()
#     plt.ylabel("Temperature (F)", fontsize=16)
#     plt.tick_params(axis='both', which='major', labelsize=16)
#
#     plt.show()

######################################
# 换个有问题的数据集 death_valley_2014.csv, 所以要做错误检查
# filename = "death_valley_2014.csv"
# with open(filename) as f:
#     reader = csv.reader(f)
#     header_row = next(reader)
#
#     dates, highs, lows = [], [], []
#
#     for row in reader:
#         try:
#             current_date = datetime.strptime(row[0].replace('/', '-'), '%Y-%m-%d')
#             high = int(row[1])
#             low = int(row[3])
#         except ValueError:
#             print(current_date, 'missing data')
#         else:
#             dates.append(current_date)
#             highs.append(high)
#             lows.append(low)
#
#     fig = plt.figure(dpi=128, figsize=(10, 6))
#     plt.plot(dates, highs, c='red', alpha=0.5)
#     plt.plot(dates, lows, c='blue', alpha=0.5)
#     plt.fill_between(dates, highs, lows, facecolor='blue', alpha=0.1)
#
#     # 设置图形的格式
#     plt.title("Daily high and low temperatures - 2014\nDeath Valley, CA", fontsize=24)
#     plt.xlabel('', fontsize=16)
#     fig.autofmt_xdate()
#     plt.ylabel("Temperature (F)", fontsize=16)
#     plt.tick_params(axis='both', which='major', labelsize=16)
#
#     plt.show()

