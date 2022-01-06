import os
from glob import glob
from test_copyright_headers import *
from cover_2_uft8 import *


def read_file(file):
    with open(file, 'r') as f:
        return f.readlines()


def write2file(file_name, lines, new_line=False):
    with open(file_name, mode='w') as fw:
        if new_line:
            fw.writelines(lines)
        else:
            fw.writelines("\n".join(sorted(lines)))


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


def check_header_exist(file_list):
    final_files = []
    for fileName in file_list:
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


def check_and_correct_tail(file_content):
    corrected = False
    for i in range(4):
        if file_content[-1] == '\n' or file_content[-1] == '\r\n':
            file_content.pop(-1)
            corrected = True
        elif '\n' not in file_content[-1].replace('\r\n', '\n'):
            file_content[-1] = file_content[-1] + '\n'
            corrected = True
            break
        else:
            break
    return [file_content, corrected]


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
                content = " " + file_content[i] if file_content[i][0] != " " else file_content[i]
        else:
            content = file_content[i]
        new_file_content.append(content)
    new_file_content = check_and_correct_tail(new_file_content)[0]
    write2file(fileName, new_file_content, True)


if __name__ == "__main__":
    path = r"C:\WorkSpace\Programming\python\Python_Work\python\format_header_tail\header"

    # 获取所有的.h和.c文件，并分别放在一个列表里
    print("1. Get all .h and .c file list...")
    h_file_list, c_file_list = get_file_list(path)
    print("-------------------------------")
    for file_list in get_file_list(path):
        # 目标文件转换为utf-8编码格式
        print("2. Covert files to utf-8 encoding...")
        covert2utf8(file_list)
        print("-------------------------------")
        # 检查文件是否有copyright，即只针对已有copyright的头文件做处理
        print("3. Check if header is existed...")
        final_files = check_header_exist(file_list)
        write2file("final_files.txt", final_files)
        print("-------------------------------")

        # 挑选出copyright检查不否规格的文件
        print("4. Filter out files that copyright checked is not correct...")
        checked_failed_files = []
        for fileName in final_files:
            if checkFile(fileName) != '':
                checked_failed_files.append(checkFile(fileName))
        write2file("copyright_checked_failed_files.txt", checked_failed_files)

        print(len(checked_failed_files), checked_failed_files)
        print("-------------------------------")

        # 把copyright检查fail的文件模板化
        print("5. Format header copyright for copyright check failed files...")
        filelist = []
        for fileName in checked_failed_files:
            update_file_header(fileName)
        print(filelist)
        print("-------------------------------")

        # 检索出copyright没问题的文件
        print("6. Get file that copyright is right, i.e. exclude check failed files")
        checked_passed_files = []
        for file in final_files:
            if file not in checked_failed_files:
                checked_passed_files.append(file)
        write2file("copyright_checked_passed_files.txt", checked_passed_files)
        print("Get the check passed files".format(checked_passed_files))
        print("-------------------------------")

        # 针对copyright没有问题的文件，检查最未尾是否有且只有一行空行，不是则更新
        print("7. For copyright passed file, to do check tail and correct...")
        for fl in checked_passed_files:
            fl_content = read_file(fl)
            if check_and_correct_tail(fl_content)[1]:
                update_file_header(fl)
        print("-------------------------------")

        print("Done")
