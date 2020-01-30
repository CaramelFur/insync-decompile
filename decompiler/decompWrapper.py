from uncompyle6 import decompile_file

def Decompyle(filein, fileout):
  f = open(fileout, "w+")
  f.seek(0)
  f.truncate(0)

  decompile_file(filein, f)

  f.flush()
  f.close()