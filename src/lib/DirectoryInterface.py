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
        if os.path.isfile(fullPath):
            size = float("{:.2f}".format(int(os.path.getsize(fullPath)) / 1000))
            lastModified = os.path.getmtime(fullPath)
            lastModified = datetime.fromtimestamp(lastModified).strftime('%H:%M:%S %m-%d-%Y')
            fileName.append(file)
            fileSize.append(size)
            modified.append(lastModified)
            print(f'\t{file}\t{size}\t{lastModified}')
        else:
            print(f'{file} is not a file, omitting from view')
    return zip(fileName, fileSize, modified)