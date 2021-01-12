'''

WoT randomizer - gun effect randomizer written by KptKosmit91

'''

import xml.etree.ElementTree as ET
import xmlMethods as xml
import config as conf
import os
import random
import fileMethods as fm

rand= conf.RandomizeGunEffectsAndSounds

if rand == "false":
    print("Gun effect randomization disabled, skipping.")
    quit()

seed=conf.seed

print("Seed: " + str(seed))

random.seed(seed)

gunFiles = []

def getFilePaths():
    for f in conf.countryFolders:
        folder = conf.tanksPath+conf.countryFolders[f]+"/components/"
        for n in os.listdir(folder):
            if n.lower() == "guns.xml":
                gunFiles.append(folder+n)

getFilePaths()

def update(gun):
    print(("Randomizing effects on guns from: " + gun))
    tree = ET.parse(gun)
    root = tree.getroot()
    gstorage = root.find("shared")

    guns = gstorage.findall("*")
    for e in guns:

        if int(seed) == 666:
            xml.insertElement("effects", "shot_superhuge", e)

            if xml.elementExists("clip", e) == False:
                xml.insertElement("reloadEffect", "reload155_170", e)

            xml.insertElement("recoilEffect", "huge", e.find("recoil"))
        else:
            rand = xml.getRandomListIndex(conf.getRandomEffects(), random)
            xml.insertElement("effects", conf.getRandomEffects()[rand], e)

            randomizeReload = False
            for eff in conf.getRandomReloadEffects():
                if xml.getElementText("reloadEffect", e) == eff:
                    randomizeReload = True
                    break

            if randomizeReload == True:
                rand = xml.getRandomListIndex(conf.getRandomReloadEffects(), random)
                xml.insertElement("reloadEffect", conf.getRandomReloadEffects()[rand], e)

            rand = xml.getRandomListIndex(conf.getRandomRecoilEffects(), random)
            xml.insertElement("recoilEffect", conf.getRandomRecoilEffects()[rand], e.find("recoil"))


    newtree = ET.ElementTree(root)

    newtree.write(gun.replace("Source", "Output"))

for e in gunFiles:
    update(e)