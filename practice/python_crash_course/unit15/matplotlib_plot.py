import matplotlib.pyplot as plt

# 1 最简单参数设置
# squares = [1, 4, 9, 25]
# plt.plot(squares)
# plt.show()

# 2
squares = [1, 4, 9, 25]
input_values = [1, 2, 3, 5]
plt.plot(input_values, squares, linewidth=5)

# 设置图标标题，并给坐标轴加上标签
plt.title("square numbers", fontsize=24)
plt.xlabel("value", fontsize=14)
plt.ylabel("square of value", fontsize=14)

# 设置刻度标记大小
plt.tick_params(axis="both", labelsize=14)
plt.show()
