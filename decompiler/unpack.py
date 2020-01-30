from os import makedirs
from header import header
from ispip import isPipModule, isLocalModule
from archive_viewer import get_all
from saveDependencies import *
from initGen import GenerateInitFile
from copydir import copyDir
from decompWrapper import Decompyle
from sys import argv, exit

if len(argv) != 3:
    print("Please pass 2 arguments")
    exit()

sourceDir = argv[1] #"./extract/sourceLib/"
exportDir = argv[2] #"./extract/code/"  # Add end slash

[archFiles, archive] = get_all(sourceDir + "insync")


def isPYI(filename):
    if filename.startswith("pyi_rth_"):
        return True
    if filename.startswith("pyimod"):
        return True
    if filename.startswith("pyiboot"):
        return True
    return False


def saveFile(location, filename, *parts):
    location = exportDir + location

    makedirs(location, exist_ok=True)
    f = open(location + filename, "wb")
    f.seek(0)
    for part in parts:
        f.write(part)
    f.close()


def saveArchFile(fileNameInArchive, fileContent):
    leadChar = fileContent[0]

    fileNameInArchiveParts = fileNameInArchive.split(".")

    isTopLevelFile = len(fileNameInArchiveParts) == 1

    moduleName = fileNameInArchiveParts[0]
    fileName = fileNameInArchiveParts.pop()

    if fileName == "insync":
        isTopLevelFile = False

    if isTopLevelFile:
        fileNameInArchiveParts.append(moduleName)

    dirName = "./" + "/".join(fileNameInArchiveParts) + "/"

    if isPYI(fileName):
        print("Skipping", fileName, "because it is a pyi file")
        return

    if not IsDependency(moduleName):
        if isLocalModule(moduleName):
            AddLocalDependency(moduleName)
            return
        if isPipModule(moduleName):
            AddPipDependency(moduleName)
            return
    else:
        return

    if leadChar == 227 or leadChar == 66:
        fileNameWithExt = fileName + ".pyc"
        print("Saving", fileNameWithExt, "from", moduleName)

        if leadChar == 227:
            saveFile(dirName, fileNameWithExt, header, fileContent)
        elif leadChar == 66:
            saveFile(dirName, fileNameWithExt, fileContent)

        if isTopLevelFile:
            saveFile(dirName, "__init__.py", GenerateInitFile(fileName))

        if fileName == "insync":
            Decompyle(exportDir + "insync.pyc", exportDir + "insync.py")

    elif leadChar == 80:
        return


def saveZlibFiles(fileDict, arch):
    for fileArchName in fileDict:
        fileArch = fileDict[fileArchName]
        fileData = fileArch[1]

        saveArchFile(fileArchName, fileData)


def saveArchFiles(fileArr, arch):
    for archFile in fileArr:
        fileInfo = archFile[0]
        fileType = type(fileInfo)

        if fileType == tuple:
            fileData = archFile[1]
            fileArchName = fileInfo[5]

            saveArchFile(fileArchName, fileData)
        elif fileType == dict:
            saveZlibFiles(fileInfo, arch)
        else:
            print("Error")


def moveSiteFiles():
    location = exportDir + "ideskui/"
    makedirs(location, exist_ok=True)
    copyDir(sourceDir + "ideskui/build/", location + "build")


makedirs(exportDir, exist_ok=True)

saveArchFiles(archFiles, archive)

moveSiteFiles()

ExportDepencies(exportDir + "requirements.txt", exportDir + ".python-version")
