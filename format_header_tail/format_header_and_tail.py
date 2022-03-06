from glob import glob
from test_copyright_headers import *
from file_handle.cover_2_uft8 import *
from file_handle.get_file_list import *
from file_handle.read_write_operator import *


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


def get_year_content(fileName):
    try:
        file_content = read_file(fileName)
        type1_flag, type2_flag = False, False
        if str(file_content[0]).strip() != "//":
            pattern = "\* Copyright\s*\(c\) (20\d\d)?(-20\d\d)? Fingerprint Cards AB <tech@fingerprints.com>"
            type1_flag = True
        else:
            pattern = "// Copyright\s*\(c\) (20\d\d)?(-20\d\d)? Fingerprint Cards AB <tech@fingerprints.com>"
            type2_flag = True

        for line, content in enumerate(file_content):
            if r"Fingerprint Cards AB <tech@fingerprints.com>" in content:
                year_line = line
                year_data = re.findall(pattern, file_content[line].strip())
                if len(year_data) != 0 and len(year_data[0]) != 0:
                    if type1_flag:
                        new_year_content = " * Copyright (c) {}-2022 Fingerprint Cards AB <tech@fingerprints.com>\n".format(
                            year_data[0][0])
                    elif type2_flag:
                        new_year_content = "// Copyright (c) {}-2022 Fingerprint Cards AB <tech@fingerprints.com>\n".format(
                            year_data[0][0])

            if line > 1 and (r"*/" in str(content).strip()[:3] or r"//" == str(content).strip()):
                header_end_line = line
                break
        print(fileName)
        return new_year_content, year_line, header_end_line
    except UnboundLocalError as e:
        print("{} raised error {}".format(fileName, e))


def new_content_write_back(fileName, new_year_content, year_line, header_end_line):
    file_content = read_file(fileName)
    new_file_content = []
    for i in range(len(file_content)):
        if i <= header_end_line:
            if i == 0:
                content = file_content[i]
            elif i == year_line:
                content = new_year_content
            else:
                if file_content[0].strip() == "//":
                    content = file_content[i]
                else:
                    content = " " + file_content[i] if file_content[i][0] != " " else file_content[i]
        else:
            content = file_content[i]
        new_file_content.append(content)

    return new_file_content


def update_file_header(fileName):
    filelist.append(fileName)

    new_year_content, year_line, header_end_line = get_year_content(fileName)

    new_file_content = new_content_write_back(fileName, new_year_content, year_line, header_end_line)

    new_file_content = check_and_correct_tail(new_file_content)[0]

    dst_path = os.path.join(os.path.dirname(fileName), os.pardir, "new", os.path.basename(fileName))
    write_file(dst_path, new_file_content, True)


if __name__ == "__main__":
    path = r"C:\WorkSpace\Programming\python\Python_Work\python\format_header_tail\testfiles"

    file_types = ["*.h", "*.c"]
    for file_type in file_types:
        # 获取所有的.h和.c文件，并分别放在一个列表里
        print("1. Get all .h and .c file list...")
        file_list = get_file_list(path, file_type)

        print("-------------------------------")
        # 目标文件转换为utf-8编码格式
        print("2. Covert files to utf-8 encoding...")
        covert2utf8(file_list)
        print("-------------------------------")
        # 检查文件是否有copyright，即只针对已有copyright的头文件做处理
        print("3. Check if header is existed...")
        final_files = check_header_exist(file_list)
        write_file("final_files.txt", final_files)
        print("-------------------------------")
        # 挑选出copyright检查不否规格的文件
        print("4. Filter out files that copyright checked is not correct...")
        checked_failed_files = []
        for fileName in final_files:
            if checkFile(fileName) != '':
                checked_failed_files.append(checkFile(fileName))
        write_file("copyright_checked_failed_files.txt", checked_failed_files)

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
        write_file("copyright_checked_passed_files.txt", checked_passed_files)
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
