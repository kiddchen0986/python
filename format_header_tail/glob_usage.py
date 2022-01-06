import os
from glob import glob

files = []
for path, folders, _ in os.walk(r"E:\WorkSpace\mtt\dev\dev4"):
    file_name = glob(os.path.join(path, "*.h"))
    files.extend(file_name)

print(len(files))
with open("list.txt", mode="w") as fw:
    for file in sorted(files):
        # print(file)
        fw.write(file+"\n")


files2 = []
for path, folders, files in os.walk(r"E:\WorkSpace\mtt\dev\dev4"):
    for file in files:
        if file.endswith(".h"):
            files2.append(os.path.join(path, file))

print(len(files2))
with open("list2.txt", mode="w") as fw:
    for file in sorted(files2):
        fw.write(file+"\n")
