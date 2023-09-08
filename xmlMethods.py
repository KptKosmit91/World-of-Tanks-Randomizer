'''

WoT randomizer xml utilities written by KptKosmit91

'''

IsWheeledTag = "RAND_IsWheeled"
IsDoubleGunTag = "RAND_IsDoubleGun"

import xml.etree.ElementTree as ET
from configLoader import Config as conf
import os

def getRandomListIndex(l, random):
    return random.randrange(0, len(l))

def insertElementEmptyNew(name, where):
    return ET.SubElement(where, name)

def insertElementEmpty(name, where):
    existingElement = where.find(name)
    if existingElement != None:
        where.remove(existingElement)
    return ET.SubElement(where, name)

def insertElement(name, value, where):
    if value !="":
        existingElement = where.find(name)
        if existingElement != None:
            existingElement.text = value
        else:
            ET.SubElement(where, name).text = value


def replace_element(new_element, where):
    """
    :param new_element:
    :param where: the section where the element will be replaced
    """
    if new_element is not None:
        name = new_element.tag
        existing_element = where.find(name)
        if existing_element is not None:
            removeAllElementsByName(name, where)
        where.append(new_element)


def replace_element_with_fallback(new_element, new_element_fallback, where):
    """
    :param new_element:
    :param new_element_fallback: will fallback to this if new_element is null
    :param where: the section where the element will be replaced
    """
    if new_element is None:
        new_element = new_element_fallback

    if new_element is not None:
        name = new_element.tag
        existing_element = where.find(name)
        if existing_element is not None:
            removeAllElementsByName(name, where)
        where.append(new_element)


def add_element(new_element, where):
    if new_element is not None:
        name = new_element.tag
        existing_element = where.find(name)
        if existing_element is not None:
            removeAllElementsByName(name, where)

    if new_element != None:
        where.append(new_element)

def getElementText(name, where):
    existingElement = where.find(name)
    if existingElement != None:
        return existingElement.text
    return "null"

def elementExists(name, where):
    existingElement = where.find(name)
    if existingElement != None:
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