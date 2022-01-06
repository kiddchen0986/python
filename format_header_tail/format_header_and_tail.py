import os
from glob import glob
from test_copyright_headers import *
from cover_2_uft8 import *


def read_file(file):
    with open(file, 'r') as f:
        return f.readlines()


def write2file(file_name, lines):
    with open(file_name, mode='w') as fw:
        fw.writelines("\n".join(lines))


def create_files_txt(file_name, files):
    print("{} file number: {} ".format(file_name[0], str(len(files))))
    with open(file_name + ".txt", mode="w") as fw:
        for file in sorted(files):
            fw.write(file+"\n")


def get_file_list(src):
    h_file_list = []
    c_file_list = []
    for path, folders, _ in os.walk(src):
        h_file_name = glob(os.path.join(path, "*.h"))
        h_file_list.extend(h_file_name)

        c_file_name = glob(os.path.join(path, "*.c"))
        c_file_list.extend(c_file_name)

    create_files_txt("h_file", h_file_list)
    create_files_txt("c_file", c_file_list)

    return h_file_list, c_file_list


def check_header_exist():
    final_files = []
    for fileName in h_file_list:
        try:
            with open(fileName, mode='r', encoding='UTF-8') as fr:
                lines = fr.readlines()
            if len(lines) > 12:
                for line in lines[:6]:
                    if "Fingerprint Cards AB <tech@fingerprints.com>" in line:
                        final_files.append(fileName)
        except UnicodeDecodeError as e:
            print("{} raise error {}".format(fileName, e))

    return final_files


def update_file_header(fileName):
    filelist.append(fileName)
    pattern = "\* Copyright\s*\(c\) (20\d\d)?(-20\d\d)? Fingerprint Cards AB <tech@fingerprints.com>"
    file_content = read_file(fileName)
    for line, content in enumerate(file_content):
        if r"Fingerprint Cards AB <tech@fingerprints.com>" in content:
            year_line = line
            year_content = re.findall(pattern, file_content[line].strip())
        if r"*/" in content:
            header_end_line = line
            break
    print("kkk"+fileName)
    if len(year_content[0]) != 0:
        new_year_content = " * Copyright (c) {}-2022 Fingerprint Cards AB <tech@fingerprints.com>\n".format(
            year_content[0][0])
    else:
        print("-------------------------")
        print("Please manually check if the file is correct header\n {}".format(fileName))
        print("-------------------------")

    new_file_content = []
    for i in range(len(file_content)):
        if i <= header_end_line:
            if i == 0:
                content = file_content[i]
            elif i == year_line:
                content = new_year_content
            else:
                content = " " + file_content[i]
        else:
            content = file_content[i]
        new_file_content.append(content)
    with open(os.path.join(os.path.dirname(fileName), os.pardir, "new", os.path.basename(fileName)), mode='w') as fw:
        fw.writelines(new_file_content)


if __name__ == "__main__":
    path = r"E:\WorkSpace\Python\python_work\python\format_header_tail\header"

    # 获取所有的.h和.c文件，并分别放在一个列表里
    h_file_list, c_file_list = get_file_list(path)
    # 目标文件转换为utf-8编码格式
    covert2utf8(h_file_list)
    # 检查文件是否有copyright，即只针对已有copyright的头文件做处理
    final_files = check_header_exist()

    # 挑选出copyright检查不否规格的文件
    checked_failed_files = []
    for fileName in final_files:
        if checkFile(fileName) != '':
            checked_failed_files.append(checkFile(fileName))
    write2file("checked_failed_files.txt", checked_failed_files)

    print(len(checked_failed_files), checked_failed_files)

    # 把failed的文件改成copyright的模板
    filelist = []
    for fileName in checked_failed_files:
        update_file_header(fileName)
        # if "@copyright" in file_content[1]:
        #     update_doxgenheader_file(fileName)
        # else:  # normalHeaderRgx
        #     update_normalHeaderRgx_file(fileName)

    print(filelist)
    # for file in checked_failed_files:
    #     i = 0
    #     with open(file, mode='r') as fr:
    #         data_content = fr.readlines()
    #         for i, data in enumerate(data_content):
    #             if "Any use is subject to an appropriate license granted by Fingerprint Cards AB" in data:
    #                 print(i, data)
    #                 break
    #     with open(file, mode='w') as fw:
    #         for data in data_content[i+2:]:
    #             fw.write(data)
