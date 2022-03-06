def func(n):
    if n==1:
        return 1
    return n * func(n-1)


result = func(5)
print("The result of 5! by using recursive call: {}".format(result))
