import os
import shutil


def move_files(foldername):
    for drive in ["c:\\", "e:\\"]:
        if os.path.exists(drive):
            for dir in os.listdir(drive):
                if "workspace" == dir.lower():
                    if ".ssh" in os.listdir(os.path.join(drive, dir)):
                        for file in os.listdir(os.path.join(drive, dir, ".ssh", foldername)):
                            if file == ".gitconfig":
                                shutil.copy(os.path.join(drive, dir, ".ssh", foldername, file), os.path.join(drive, dir))
                            else:
                                shutil.copy(os.path.join(drive, dir, ".ssh", foldername, file), os.path.join(drive, dir, ".ssh"))
                        break
                    else:
                        print("Don't have the .ssh folder")
    print("Files in {} copy finished!".format(foldername))


if __name__ == "__main__":
    print("Choice which kind of github: FPC is 1, Private is 2: ")
    choice = int(input())
    if 1 == choice:
        move_files("FPC")
    elif 2 == choice:
        move_files("Private")
    else:
        print("Your choice is wrong!")
        exit()
