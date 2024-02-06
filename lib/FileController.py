#! /usr/bin/env python3

import os
from datetime import datetime

def GetDirectoryContents(path):
    contents = os.listdir(path)
    fileName : str = []
    fileSize : str = []
    modified : str = [] 

    for file in contents:
        fullPath = os.path.join(path, file)
        size = os.path.getsize(fullPath)
        lastMod = os.path.getmtime(fullPath)
        lastMod = datetime.fromtimestamp(lastMod).strftime('%H:%M:%S %m-%d-%Y')
        fileName.append(file)
        fileSize.append(size)
        modified.append(lastMod)
        print(f'\t{file}\t{size}\t{lastMod}')

    return zip(fileName, fileSize, modified)

