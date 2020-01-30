def GenerateInitFile(fileToImportFrom):
    string = "from ." + fileToImportFrom + " import *\n" \
    "try:\n" \
    "\tfrom ." + fileToImportFrom + " import __VERSION__\n" \
    "except:\n" \
    "\tpass\n"
    return bytes(string, 'utf-8')
