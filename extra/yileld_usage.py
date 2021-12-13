from collections import OrderedDict


def fab(max):
    ordered_dict = {}
    n, a, b = 0, 0, 1
    while n < max:
        ordered_dict["a"] = a
        ordered_dict["b"] = b
        yield ordered_dict
        a, b = b, a + b
        n = n + 1


data_temp = []
data_temp.extend(fab(5))
print(data_temp)
