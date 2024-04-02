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

os.chdir(sourceDir)

for root, dirs, files in os.walk("."):
    for file in files:
        sourceFile = join(root, file)
        fileList.append((join(mirrorDir, sourceFile), get_md5(sourceFile)))
    for dir in dirs:
        sourceDir = join(root, dir)
        dirList.append(join(mirrorDir, sourceDir))

for dir in dirList:
    os.makedirs(dir)
    print(dir)

for file in fileList:
    fileName = file[0]
    mirrorFileContent = file[1]

    with open(fileName+".txt", "w") as f:
        f.write(mirrorFileContent)
        print(fileName, mirrorFileContent)
