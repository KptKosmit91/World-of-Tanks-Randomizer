# -*- coding: utf-8 -*-

'''

WoT randomizer - file utilities written by KptKosmit91

'''

import os
import pathlib

def createFolder(name):
    if not os.path.exists(name):
        #print("Creating folder '" + name + "'.")\
        pathlib.Path(name).mkdir(parents=True, exist_ok=True)
    # else:
    #     print("Folder '" + name + "' already exists.")

def createFile(name, content):
    file = open(name, 'w')
    file.write(content)
    file.close()

def createFileWithWarning(name, error, content):
    if not os.path.exists(name):
        createFile(name, content)
    else:
        shouldCreate = str(input("File " + name + " already exists. Should it be overwriten? (Y/N) " + error + " "))
        if shouldCreate.lower() == "y" or shouldCreate.lower() == "yes":
            createFile(name, content)
        else:
            print("Keeping previous " + name)