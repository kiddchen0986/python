import os
from filehandle.get_file_list import *
from filehandle.read_write_operator import *


path = r"C:\WorkSpace\Programming\python\Python_Work\python\format_header_tail\testfiles"


try:
    for file in get_file_list(path, "*.c"):
        print(file)
        file_content = read_file(file)
        new_file_content = []
        for content in file_content:
            if "Ã‚Âµm" in content:
                content = content.replace('Ã‚Âµm', 'um')
                print('convert {} to {}'.format('Ã‚Âµm', 'um'))
            if 'Ã‚ÂµA' in content:
                content = content.replace('Ã‚ÂµA', 'uA')
                print('convert {} to {}'.format('Ã‚ÂµA', 'uA'))
            if "Âµm" in content:
                content = content.replace("Âµm", 'um')
                print('convert {} to {}'.format("Âµm", 'um'))
            if "µm" in content:
                content = content.replace("µm", 'um')
                print('convert {} to {}'.format("µm", 'um'))
            if 'Â' in content:
                content = content.replace('Â', '')
                print('convert {} to {}'.format('Â', ''))
            if "Î¼A" in content:
                content = content.replace('Î¼A', 'uA')
                print("convert {} to {}".format('Î¼A', "uA"))
            if "â€¬" in content or 'â€' in content or 'â€­' in content:
                content = content.replace('â€¬', ' ').replace('â€­', ' ').replace('â€', ' ')
                print('convert {} to {}'.format('â€¬', ' '))
            if 'Î¼V' in content:
                content = content.replace('Î¼V', 'uV')
                print('convert {} to {}'.format('Î¼V', 'uV'))
            if 'ÃŽÂ¼V' in content:
                content = content.replace('ÃŽÂ¼V', 'uV')
                print('convert {} to {}'.format('ÃŽÂ¼V', 'uV'))
            new_file_content.append(content)

        write2file(file, new_file_content, True)
except UnicodeDecodeError as e:
    print("{} raised error {}".format(file, e))



