import os
__thisDir = os.path.split(os.path.realpath(__file__))[0]

f = open(__thisDir + "/header.bin", "rb")
header = f.read(16)
f.close()