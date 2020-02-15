import xml.etree.ElementTree as ET
import xmlMethods as xml
import config as conf
import os
import random
import fileMethods as fm
from shutil import copyfile

if conf.RandomizeMusicOnMaps == "false":
    print("Map music randomizing disabled, skipping.")
    quit()

seed=conf.seed

randCustom = conf.CustomSounds
randName = conf.RandomizeMapNames
randNameTanks = conf.RandomizeMapNamesWithTankNames
randFoliage = conf.RandomizeFoliageColor

if randCustom == "false" and randName == "false" and randNameTanks == "false" and randFoliage == "false":
    quit

randNameMode = "none"

if randName == "true":
    randNameMode = "norm"
if randNameTanks == "true":
    randNameMode = "tank"

print("Seed: " + str(seed))

random.seed(seed)

maps = []
tankLists = []

tankListsXmls = []
mapXmls = []
mapXmlsIntensive = []
mapXmlsRelaxed = []
mapXmlsWin = []
mapXmlsDraw = []
mapXmlsDefeat = []
mapXmlsName = []
mapXmlsDesc = []
tanks = []

def getFilePaths():
    folder = conf.mapsPath
    for n in os.listdir(folder):
        if n.lower() != "_default_.xml" and n.lower() != "_list_.xml" and n.lower() != "hangar_v3.xml" and n.lower() != "1002_ai_test.xml":
            if randCustom == "true":
                maps.append(folder+n)
            elif not n.startswith("dummy"):
                maps.append(folder+n)

    #get tonk lists
    if randNameMode == "tank":
        for f in conf.countryFolders:
            folder = conf.tanksPath+conf.countryFolders[f]+"/"
            for n in os.listdir(folder):
                if  n.lower() == "list.xml":
                    tankLists.append(folder+n)
                    break


def getMaps(m):
    tree = ET.parse(m)
    root = tree.getroot()

    mapXmls.append(root)
    mapXmlsDefeat.append(root)
    mapXmlsDraw.append(root)
    mapXmlsIntensive.append(root)
    mapXmlsRelaxed.append(root)
    mapXmlsWin.append(root)

    if randNameMode == "norm" and not m.replace(conf.mapsPath, "").startswith("dummy"):
        mapXmlsName.append(root)
        mapXmlsDesc.append(root)

def getTankList(t):
    tree = ET.parse(t)
    root = tree.getroot()

    tankListsXmls.append(root)

    for t in tankListsXmls:
        for i in t.findall("*"):
            tanks.append(i)


def randomizeFoliageColors(m, customName):
    if randFoliage == "true":
        tints = []
        treeTintsPath = "Source/res/spaces/trees_tint_maps/"
        for n in os.listdir(treeTintsPath):
            if n.lower().endswith(".dds"):
                tints.append(treeTintsPath+n)

        rand = xml.getRandomListIndex(tints, random)
        mapName = m.replace(conf.mapsPath, "").replace(".xml", "")
        path = "Output/res/spaces/" + mapName + "/"

        if not os.path.exists(path):
            os.mkdir(path)
        
        copyfile(tints[rand], path + customName + ".dds")

def updateMap(m):
    if m.replace(conf.mapsPath, "").startswith("dummy"):
        return None

    print(("Randomizing Things on Map: " + m))

    tree = ET.parse(m)
    root = tree.getroot()

    if randNameMode == "norm":

        rand = xml.getRandomListIndex(mapXmlsName, random)
        xml.addElement("name", mapXmlsName[rand].find("name"), root)
        mapXmlsName.pop(rand)

        rand = xml.getRandomListIndex(mapXmlsDesc, random)
        xml.addElement("description", mapXmlsDesc[rand].find("description"), root)
        mapXmlsDesc.pop(rand)

    if randNameMode == "tank":

        rand = xml.getRandomListIndex(tanks, random)
        xml.insertElement("name", tanks[rand].find("userString").text, root)
        tanks.pop(rand)

        rand = xml.getRandomListIndex(tanks, random)
        xml.addElement("description", tanks[rand].find("description"), root)
        tanks.pop(rand)

    musicSetup = root.find("wwmusicSetup")

    rand = xml.getRandomListIndex(mapXmls, random)
    xml.addElement("wwmusicLoading", mapXmls[rand].find("wwmusicSetup").find("wwmusicLoading"), musicSetup)
    mapXmls.pop(rand)

    rand = xml.getRandomListIndex(mapXmlsIntensive, random)
    xml.addElement("wwmusicIntensive", mapXmlsIntensive[rand].find("wwmusicSetup").find("wwmusicIntensive"), musicSetup)
    mapXmlsIntensive.pop(rand)

    rand = xml.getRandomListIndex(mapXmlsRelaxed, random)
    xml.addElement("wwmusicRelaxed", mapXmlsRelaxed[rand].find("wwmusicSetup").find("wwmusicRelaxed"), musicSetup)
    mapXmlsRelaxed.pop(rand)

    rand = xml.getRandomListIndex(mapXmlsWin, random)
    xml.addElement("wwmusicResultWin", mapXmlsWin[rand].find("wwmusicSetup").find("wwmusicResultWin"), musicSetup)
    mapXmlsWin.pop(rand)

    rand = xml.getRandomListIndex(mapXmlsDraw, random)
    xml.addElement("wwmusicResultDrawn", mapXmlsDraw[rand].find("wwmusicSetup").find("wwmusicResultDrawn"), musicSetup)
    mapXmlsDraw.pop(rand)

    rand = xml.getRandomListIndex(mapXmlsDefeat, random)
    xml.addElement("wwmusicResultDefeat", mapXmlsDefeat[rand].find("wwmusicSetup").find("wwmusicResultDefeat"), musicSetup)
    mapXmlsDefeat.pop(rand)

    
    newtree = ET.ElementTree(root)

    newtree.write(m.replace("Source", "Output"))

    randomizeFoliageColors(m, 'trees_tint_map')

    return None

getFilePaths()

for m in maps:
    getMaps(m)

if randNameMode == "tank":
    for t in tankLists:
        getTankList(t)

for m in maps:
    updateMap(m)

randomizeFoliageColors("Source/res/scripts/arena_defs/hangar_v3", "flora_tint_map")