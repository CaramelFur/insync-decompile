import requests
import sys
import pkgutil

allPackages = []

for d in pkgutil.iter_modules():
    allPackages.append(d.name)

allPackages.sort()

#print(allPackages)

def isPipModule(neg):
    r = requests.get('https://pypi.org/simple/' + neg + '/')
    code = r.status_code
    return code == 200

def isLocalModule(neg):
    if(neg in allPackages):
            return True


