import os
from filehandle.get_file_list import *
from filehandle.read_write_operator import *


path = r"C:\WorkSpace\Programming\python\Python_Work\python\format_header_tail\header"


try:
    for file in get_file_list(path, "*.h"):
        print(file)
        file_content = read_file(file)
        new_file_content = []
        for content in file_content:
            if "Ã‚Âµm" in content or "Âµm" in content or "µm" in content or 'Ã‚ÂµA' in content:
                content = content.replace('Ã‚Âµm', 'um').replace('Ã‚ÂµA', 'uA').replace('µm', 'um').replace('Â', '')
            if "Î¼A" in content:
                content = content.replace('Î¼A', 'uA')
                print("convert {} to {}".format('Î¼A', "uA"))
            new_file_content.append(content)

        dst_path = os.path.join(os.path.dirname(file), os.pardir, "../format_header_tail/replace_µm", os.path.basename(file))
        write2file(dst_path, new_file_content, True)
except UnicodeDecodeError as e:
    print("{} raised error {}".format(file, e))



