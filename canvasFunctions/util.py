import os, csv, sys
from pathlib import Path

# Creates the file and writes the headers to the file
def fileCreate(fileName, headers=None):
   path = str(Path.home() / "Downloads" / fileName)
   f = os.open(path, os.O_RDWR | os.O_CREAT, 0o666)
   fd = os.fdopen(f, "x", newline='')
   writer = csv.writer(fd)
   writer.writerow(headers)
   return writer

def getSubset(data, keys):
   subset = [data.get(key) for key in keys]
   return subset

def getDictSubset(data, keys):
   subset = {key: data.get(key) for key in keys}
   return subset