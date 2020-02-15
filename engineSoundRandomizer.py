import xml.etree.ElementTree as ET
import xmlMethods as xml
import config as conf
import os
import random
import fileMethods as fm

randSounds = conf.RandomizeEngineSounds
randRPM = conf.RandomizeEngineRPM

if randSounds == "false" and randRPM == "false":
    print("Engine sound and RPM randomizing disabled, skipping.")
    quit()

seed=conf.seed

print("Seed: " + str(seed))

random.seed(seed)

engineFiles = []

rpm_minMin = 0
rpm_minMax = 0

rpm_maxMin = 0
rpm_maxMax = 0

if randRPM == "true":
    rpm_minMin = conf.rpm_minMin
    rpm_minMax = conf.rpm_minMax

    rpm_maxMin = conf.rpm_maxMin
    rpm_maxMax = conf.rpm_maxMax

def getFilePaths():
    for f in conf.countryFolders:
        folder = conf.tanksPath+conf.countryFolders[f]+"/components/"
        for n in os.listdir(folder):
            if n.lower() == "engines.xml":
                engineFiles.append(folder+n)

getFilePaths()

npcSounds = conf.getEngineSFX("NPC")
pcSounds = conf.getEngineSFX("PC")

def update(engine):
    if randSounds == "true":
        print(("Randomizing sound on engines from: " + engine))
    tree = ET.parse(engine)
    root = tree.getroot()
    estorage = root.find("shared")

    engines = estorage.findall("*")
    for e in engines:

        if randSounds == "true":
            if int(seed) == 666:
                xml.insertElement("wwsoundNPC", "eng_ContinentalR_npc", e)
                xml.insertElement("wwsoundPC", "eng_ContinentalR_pc", e)
            else:
                rand = xml.getRandomListIndex(npcSounds, random)
                xml.insertElement("wwsoundNPC", npcSounds[rand], e)

                rand = xml.getRandomListIndex(npcSounds, random)
                xml.insertElement("wwsoundPC", pcSounds[rand], e)

        if randRPM == "true":
            xml.insertElement("rpm_min", str(random.randrange(rpm_minMin, rpm_minMax)), e)
            xml.insertElement("rpm_max", str(random.randrange(rpm_maxMin, rpm_maxMax)), e)

    newtree = ET.ElementTree(root)

    newtree.write(engine.replace("Source", "Output"))

for e in engineFiles:
    update(e)