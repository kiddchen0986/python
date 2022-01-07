import os


def read_file(file):
    with open(file, 'r') as f:
        return f.readlines()


def write_file(file_name, lines, new_line=False):
    with open(file_name, mode='w') as fw:
        if new_line:
            fw.writelines(lines)
        else:
            fw.writelines("\n".join(sorted(lines)))


def read_binary_file(file):
    with open(file, 'rb') as f:
        return f.read()


def write_binary_file(content, file):
    with open(file, 'wb') as f:
        f.write(content)
