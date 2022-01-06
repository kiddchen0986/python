import os
#files = os.listdir(".")#获取当前目录下的文件
from chardet.universaldetector import UniversalDetector


def get_filelist(path):
    Filelist = []
    for home, dirs, files in os.walk(path):
        for filename in files:
            # 文件名列表，包含完整路径
            if ".h" in filename:
                Filelist.append(os.path.join(home, filename))
            # # 文件名列表，只包含文件名
            # Filelist.append( filename)

    return Filelist


def get_encode_info(file):
    with open(file, 'rb') as f:
        detector = UniversalDetector()
        for line in f.readlines():
            detector.feed(line)
            if detector.done:
                break
        detector.close()
        return detector.result['encoding']


def read_file(file):
    with open(file, 'rb') as f:
        return f.read()


def write_file(content, file):
    with open(file, 'wb') as f:
        f.write(content)


def convert_encode2utf8(file, original_encode, des_encode):
    file_content = read_file(file)
    file_decode = file_content.decode(original_encode,'ignore')
    file_encode = file_decode.encode(des_encode)
    write_file(file_encode, file)


def covert2utf8(Filelist):
    # Filelist = get_filelist(path)
    for filename in Filelist:
        file_content = read_file(filename)
        encode_info = get_encode_info(filename)
        if encode_info != 'utf-8':
            convert_encode2utf8(filename, encode_info, 'utf-8')
        encode_info = get_encode_info(filename)
        print(encode_info)


# if __name__ == "__main__":
#     Path = r'E:\WorkSpace\Python\python_work\python\file_practice\.h'
#     covert2utf8(Path)