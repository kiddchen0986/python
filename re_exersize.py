import re

txt = '''
万门大学老师：正正
万门大学老师：kk
万门大学老师：培培
万门大学老师：陈王

'''

pattern = r"：(.*)"    # . 除换行的以外的任意字符，* 前边子表达式匹配任意次数，包含0次。
result = re.findall(pattern, txt)
print(result)

info= '''
mike，18301011111，39
lin，13932111111，40
danial，15932431115，45
frank，1A932431115，45
'''
pattern_phone_no = r"[1-9][0-9]{4,11}"  # r"\d{11}"
result = re.findall(pattern_phone_no, info)
print(result)

qq = '78929302@qq.com'
pattern = r"\d{8}@[0-9a-z]*.com"
res = re.match(pattern, qq)
print(bool(res))

info = "pyabc-001"
pattern = "abc\-001"
res = re.findall(pattern, info)
print(res)


pattern = r"^(\d{3})-(\d{3,8})$"
info = "010-12345"
res = re.match(pattern, info)
print(res, res[0], res[1], res[2])


res = re.match(r'^(\d+?)(0*)$', '102300')
print(res, res[0], res[1], res[2])
