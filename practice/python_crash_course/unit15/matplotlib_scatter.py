import matplotlib.pyplot as plt

# # 1 最简单
# plt.scatter(2, 4, s=200)
#
# # 设置图表标题并给坐标轴加上标签
# plt.title("Square Numbers", fontsize=24)
# plt.xlabel("Value", fontsize=14)
# plt.ylabel("Square of Value", fontsize=14)
#
# # 设置刻度标记的大小
# plt.tick_params(axis="both", which='major', labelsize=14)
#
# plt.show()

###########################################
# # 2
# x_value = [1, 2, 3, 4, 5]
# y_value = [1, 4, 9, 16, 25]
# plt.scatter(x_value, y_value, s=200)
#
# # 设置图表标题并给坐标轴加上标签
# plt.title("Square Numbers", fontsize=24)
# plt.xlabel("Value", fontsize=14)
# plt.ylabel("Square of Value", fontsize=14)
#
# # 设置刻度标记的大小
# plt.tick_params(axis="both", which='major', labelsize=14)
#
# plt.show()

###########################################
# # # 3
# x_value = list(range(1, 1001))
# y_value = [x**2 for x in range(1, 1001)]
# plt.scatter(x_value, y_value, c='red', edgecolors='none', s=40)  # c=(0, 0, 0.8)
#
# # 设置图表标题并给坐标轴加上标签
# plt.title("Square Numbers", fontsize=24)
# plt.xlabel("Value", fontsize=14)
# plt.ylabel("Square of Value", fontsize=14)
#
# # 设置刻度标记的大小
# plt.tick_params(axis="both", which='major', labelsize=14)
# plt.axis([0, 1100, 0, 1100000])
#
# plt.show()

##################################################

