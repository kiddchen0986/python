import os
import shutil


def move_files(foldername):
    try:
        for drive in ["c:\\", "e:\\"]:
            if os.path.exists(drive):
                for dir in os.listdir(drive):
                    if "workspace" == dir.lower():
                        if ".ssh" in os.listdir(os.path.join(drive, dir)):
                            for file in os.listdir(os.path.join("license", foldername.lower())):
                                if os.path.isfile(os.path.join("license", foldername.lower(), file)):
                                    print("Copying {}".format(file))
                                    if ".gitconfig" == file:
                                        shutil.copy(os.path.join("license", foldername, file), os.path.join(drive, dir))
                                    else:
                                        shutil.copy(os.path.join("license", foldername, file),
                                                    os.path.join(drive, dir, ".ssh"))
                            break
                        else:
                            print("Don't have the .ssh folder")
    except FileNotFoundError as e:
        print("{} not found error".format(e))
    print("Files in {} folder are copied finished!".format(foldername))


if __name__ == "__main__":
    print("Choice which kind of github: Company is 1, Private is 2: ")
    choice = int(input())
    if 1 == choice:
        move_files("FPC")
    elif 2 == choice:
        move_files("Private")
    else:
        print("Your choice is wrong!")
        exit()
