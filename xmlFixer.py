'''

WoT randomizer XML fixer written by KptKosmit91
does changes to Source XML files to work with the randomizer
update tool only - used for updating the randomizer for new WoT versions

'''

import xml.etree.ElementTree as ET
import xmlMethods as xml
import config as conf
import os
import fileMethods as fm


maps = []

def loadMaps():
    folder = conf.mapsPath
    for n in os.listdir(folder):
        if n.lower() != "_default_.xml" and n.lower() != "_list_.xml" and n.lower() != "hangar_v3.xml" and n.lower() != "1002_ai_test.xml":
            maps.append(folder+n)

loadMaps()

for m in maps:
    f = open(m, "r")
    mapName = m.replace(conf.mapsPath, "").replace("	","")
    text=f.read()
    text = text.replace(mapName,"root")

    f.close()

    f = open(m, "w")
    f.write(text)
    f.close()

def getTankFilePaths():
    tanks = []
    for f in conf.countryFolders:
        folder = conf.tanksPath+conf.countryFolders[f]+"/"
        if os.path.exists(folder):
            for n in os.listdir(folder):
                if n.lower() != "components" and n.lower() != "customization.xml" and n.lower() != "list.xml":
                    tanks.append(folder+n)

        folder = conf.addonNewTankModelsVehiclesPath+conf.countryFolders[f]+"/"
        if os.path.exists(folder):
            for n in os.listdir(folder):
                if n.lower() != "components" and n.lower() != "customization.xml" and n.lower() != "list.xml":
                    tanks.append(folder+n)

        folder = conf.tanksPath.replace("Source/", "SourceOverrides/")+conf.countryFolders[f]+"/"
        if os.path.exists(folder):
            for n in os.listdir(folder):
                if n.lower() != "components" and n.lower() != "customization.xml" and n.lower() != "list.xml":
                    tanks.append(folder+n)

    return tanks

def work(tank):
    print(tank)
    tree = ET.parse(tank)
    root = tree.getroot()

    chassis = root.find("chassis").findall("*")

    xml.insertElement(xml.IsWheeledTag, "false", root)

    for c in chassis:
        nonTrack = c.find("wheels").find("wheel").find("nonTrack")
        if nonTrack is not None and nonTrack.text.lower() == "true":
            xml.insertElement(xml.IsWheeledTag, "true", root)
            break

    for t in root.find("turrets0").findall("*"):
        for g in t.find("guns").findall("*"):
            if xml.elementExists("multiGunEffects", g):
                xml.insertElement(xml.IsDoubleGunTag, "true", g)
            else:
                xml.insertElement(xml.IsDoubleGunTag, "false", g)

    newtree = ET.ElementTree(root)

    newtree.write(tank)

tanks = getTankFilePaths()

for t in tanks:
    f = open(t, "r")
    text=f.read()
    text = text.replace("	","").replace("<xmlns:xmlref>http://bwt/xmlref</xmlns:xmlref>","")

    f.close()

    f = open(t, "w")
    f.write(text)
    f.close()

for t in tanks:
    work(t)