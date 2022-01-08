from copy import copy, deepcopy


class mobilephone():
    def __init__(self, cpu, screen):
        self.cpu = cpu
        self.screen = screen


class cpu():
    def calcuate(self):
        print("To do calcuate 123...")
        print("This is cpu function...")


class screen():
    def dispaly(self):
        print("Display whatever you want...")


# just copy variable
c1 = cpu()
c2 = c1
print(c1)
print(c2)
# 浅 copy
s1 = screen()
m1 = mobilephone(c1, s1)
m2 = copy(m1)
print(m1, m1.cpu, m1.screen)
print(m2, m2.cpu, m2.screen)
# 深 copy
m2 = deepcopy(m1)
print(m1, m1.cpu, m1.screen)
print(m2, m2.cpu, m2.screen)

d1 = [1, 2, 3, 4]
d2 = d1
print(d1, d2, id(d1), id(d2))
d3 = copy(d1)
print(id(d1), id(d3))
d4 = deepcopy(d1)
print(id(d4), id(d1))

d1.append(9)
print(d1, d2, d3, d4)