from ispip import isLocalModule

__pipModules = []
__localModules = []

if not isLocalModule("pycurl"):
    __pipModules.append("pycurl")

def __remapPipModules(mod):
    if mod == "gi":
        return "pygobject"
    if mod == "xdg":
        return "pyxdg"
    if mod == "crypto":
        return "pycrypto"
    return mod


def IsDependency(dep):
    if dep in __pipModules:
        return True
    if dep in __localModules:
        return True
    return False


def AddPipDependency(dep):
    dep = __remapPipModules(dep)
    __pipModules.append(dep)


def AddLocalDependency(dep):
    __localModules.append(dep)


def ExportDepencies(location, versionlocation):
    pipModulesText = "\n".join(__pipModules)
    #localModulesText = "\n".join(__localModules)

    reqtxt = open(location, "w+")
    reqtxt.seek(0)
    reqtxt.truncate(0)
    reqtxt.write(pipModulesText)
    reqtxt.close()

    reqtxt = open(versionlocation, "w+")
    reqtxt.seek(0)
    reqtxt.truncate(0)
    reqtxt.write("3.7.4\n")
    reqtxt.close()

    print("Pip:\n", __pipModules)
    print("local:\n", __localModules)
