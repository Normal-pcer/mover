import os
import json
from os.path import join


def get_md5(s: str):
    import hashlib
    hash_obj = hashlib.md5(s.encode(encoding="UTF-8"))
    return hash_obj.hexdigest()


configFile = open("config.json", "r")
config = json.loads(configFile.read())
configFile.close()

sourceDir = config["source"]
mirrorDir = config["mirror"]

fileList = list()
dirList = list()
hashList = list()

os.chdir(sourceDir)

for root, dirs, files in os.walk("."):
    for file in files:
        sourceFile = join(root, file)
        hashList.append(get_md5(sourceFile))
        fileList.append(sourceFile)

os.chdir(mirrorDir)
logText = ""
moves = list()

for root, dirs, files in os.walk("."):
    for file in files:
        fileName = join(root, file)
        with open(fileName, "r") as f:
            hash = f.read()
            if hash in hashList:
                mirrorFileName = fileName[:-4]
                index = hashList.index(hash)
                sourceFileName = fileList[index]

                if sourceFileName != mirrorFileName:
                    print(sourceFileName, "->", mirrorFileName, hash)
                    logText += ("{} {} {} {}\n".format(sourceFileName,
                                "->", mirrorFileName, hash))
                    moves.append((sourceFileName, mirrorFileName))
    for dir in dirs:
        dirList.append(join(root, dir))

with open("log.txt", "w", encoding="UTF-8") as f:
    f.write(logText)

os.system("notepad log.txt")
confirm = input("Confirm?(Y/N): ")

os.chdir(sourceDir)
if confirm in ("Y", "y"):
    for dir in dirList:
        if not os.path.exists(dir):
            os.makedirs(dir)
            print("make", dir)
    
    for move in moves:
        import shutil
        shutil.move(move[0], move[1])
        print(move[0], "=>", move[1])
