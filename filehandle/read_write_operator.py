import os


def read_file(file):
    with open(file, 'r') as f:
        return f.readlines()


def write2file(file_name, lines, new_line=False):
    with open(file_name, mode='w') as fw:
        if new_line:
            fw.writelines(lines)
        else:
            fw.writelines("\n".join(sorted(lines)))


# def create_txt_files(file_name, files):
#     print("{} file number: {} ".format(file_name[0], str(len(files))))
#     with open(file_name + ".txt", mode="w") as fw:
#         for file in sorted(files):
#             fw.write(file+"\n")
