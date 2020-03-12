IsWheeledTag = "RAND_IsWheeled"
IsDoubleGunTag = "RAND_IsDoubleGun"

import xml.etree.ElementTree as ET
import config as conf
import os

def getRandomListIndex(l, random):
    return random.randrange(0, len(l))

def insertElementEmptyNew(name, where):
    return ET.SubElement(where, name)

def insertElementEmpty(name, where):
    existingElement = where.find(name)
    if existingElement is not None:
        where.remove(existingElement)
    return ET.SubElement(where, name)

def insertElement(name, value, where):
    if value !="":
        existingElement = where.find(name)
        if existingElement is not None:
            existingElement.text = value
        else:
            ET.SubElement(where, name).text = value

def replaceElement(name, newElement, where):
    if newElement != None:
        existingElement = where.find(name)
        if existingElement is not None:
            removeAllElementsByName(name, where)
            where.append(newElement)

def addElement(name, newElement, where):
    existingElement = where.find(name)
    if existingElement is not None:
        removeAllElementsByName(name, where)

    if newElement != None:
        where.append(newElement)

def getElementText(name, where):
    existingElement = where.find(name)
    if existingElement is not None:
        return existingElement.text
    return "null"

def elementExists(name, where):
    existingElement = where.find(name)
    if existingElement is not None:
        return True
    return False

def removeAllElementsByName(name, where):
    for e in where.findall(name):
        #print("removed" + str(e))
        where.remove(e)

def getMapFilePaths():
    maps = []
    folder = conf.mapsPath
    for n in os.listdir(folder):
        if n.lower() != "_default_.xml" and n.lower() != "_list_.xml" and n.lower() != "hangar_v3.xml" and n.lower() != "1002_ai_test.xml":
            maps.append(folder+n)
    return maps