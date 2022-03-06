from file_handle.read_write_operator import *
from glob import glob


def get_file_list(src, file_type):
    file_list = []
    for path, folders, _ in os.walk(src):
        files = glob(os.path.join(path, file_type))
        file_list.extend(files)

    print("{} file number: {}".format(str(file_type).split(".")[1], len(file_list)))
    write_file(str(file_type).split(".")[1]+"_file_list", file_list)

    return file_list
