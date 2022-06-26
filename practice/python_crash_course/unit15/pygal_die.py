import pygal
from random import randint

class Die():

    def __init__(self, num_sides=6):
        self.num_sides = num_sides

    def roll(self):
        return randint(1, self.num_sides)


# 掷一颗
# die = Die()
#
# results = []
# for roll_num in range(100):
#     result = die.roll()
#     results.append(result)
#
# print(results)
#
# frequences = []
# for i in range(1, 7):
#     frequence = results.count(i)
#     frequences.append(frequence)
#
# hist = pygal.Bar()
# hist.title = 'Statics of side'
# hist.x_labels = list(range(1, 7))
# hist.x_title = 'sides'
# hist.y_labels = list(range(0, 50))
# hist.y_title = 'Number of sides'
#
# hist.add("D6", frequences)
# hist.render_to_file("Die.svg")

#########################################
# 掷两颗
# die1 = Die()
# die2 = Die()
#
# results = []
# for roll_num in range(100):
#     result = die1.roll() + die2.roll()
#     results.append(result)
#
# print(results)
#
# frequences = []
# for i in range(2, 13):
#     frequence = results.count(i)
#     frequences.append(frequence)
#
# hist = pygal.Bar()
# hist.title = 'Statics of side'
# hist.x_labels = list(range(2, 14))
# hist.x_title = 'sides'
# # hist.y_labels = list(range(0, 50))
# hist.y_title = 'Number of sides'
#
# hist.add("2 D6", frequences)
# hist.render_to_file("Die2.svg")

######################################################
# 掷两颗面数不同的骰子
# die1 = Die()
# die2 = Die(10)
#
# results = []
# for roll_num in range(100):
#     result = die1.roll() + die2.roll()
#     results.append(result)
#
# print(results)
#
# frequences = []
# for i in range(1, 17):
#     frequence = results.count(i)
#     frequences.append(frequence)
#
# hist = pygal.Bar()
# hist.title = 'Statics of side'
# hist.x_labels = list(range(1, 18))
# hist.x_title = 'sides'
# # hist.y_labels = list(range(0, 50))
# hist.y_title = 'Number of sides'
#
# hist.add("D6 and D10", frequences)
# hist.render_to_file("Die3.svg")

###############################################

