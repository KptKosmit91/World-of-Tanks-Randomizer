import xml.etree.ElementTree as ET
import xmlMethods as xml
import config as conf
import os
from shutil import rmtree
import random
import fileMethods as fm

randModels=conf.RandomizeTankModels
randGunFX=conf.RandomizeGunEffectsAndSounds

if randModels == "false" and randGunFX == "false":
    print("Tank model and gun sounds randomizing disabled, skipping.")
    quit()

seed=conf.seed

print("Seed: " + str(seed))

seed = int(seed)

random.seed(seed)

tanks = []

tankXmlStorage = []

isChaos = conf.chaosModeEnabled.lower()

hullModels = []
turrets = []
guns = []

def getFilePaths():
    for f in conf.countryFolders:
        folder = conf.tanksPath+conf.countryFolders[f]+"/"
        for n in os.listdir(folder):
            if n.lower() != "components" and n.lower() != "customization.xml" and n.lower() != "list.xml" and not conf.isBlacklisted(n):
                tanks.append(folder+n)

def getTankModels(tank):
    tree = ET.parse(tank)
    root = tree.getroot()

    if randModels == "true":
        hull = root.find("hull")


        tankXmlStorage.append(root)
        hullModels.append(hull.find("models"))
    
    for t in root.find("turrets0").findall("*"):
        turrets.append(t)
        for g in t.find("guns").findall("*"):
            guns.append(g)


def updateTankModels(tank):
    if randModels == "true":
        print(("Randomizing Tank: " + tank).replace(conf.tanksPath, "").title())

    tree = ET.parse(tank)
    root = tree.getroot()
    if randModels == "true":
        rand = xml.getRandomListIndex(hullModels, random)

        xml.insertElement("nodes", tankXmlStorage[rand].find("hull").find("exhaust").find("nodes").text, root.find("hull").find("exhaust"))

        if conf.SensitivityToImpulseMin >= 0 and conf.SensitivityToImpulseMax >= 0:
            swinging = root.find("hull").find("swinging")

            if isChaos == "true":
                xml.insertElement("pitchParams", "0.34 66.00 0.36 1.00 91.05 0.34", swinging)
                xml.insertElement("rollParams", "0.91 0.34 45.00 0.36 1.00 91.06 0.40", swinging)
                xml.insertElement("sensitivityToImpulse", "291.94", swinging)
            else:
                xml.insertElement("sensitivityToImpulse", str(random.uniform(conf.SensitivityToImpulseMin, conf.SensitivityToImpulseMax)), swinging)

        randomModel = hullModels[rand]
        xml.addElement("models", randomModel, root.find("hull"))

        clanSlot = None
        for s in root.find("hull").find("customizationSlots").findall("slot"):
            if s.find("slotType").text.replace("	", "") == "clan":
                clanSlot = s
                break

        newClanSlot = None

        for s in tankXmlStorage[rand].find("hull").find("customizationSlots").findall("slot"):
            if s.find("slotType").text.replace("	", "") == "clan":
                newClanSlot = s
                break

        if newClanSlot is not None and clanSlot is not None:
            xml.addElement("rayStart", newClanSlot.find("rayStart"), clanSlot)
            xml.addElement("rayEnd", newClanSlot.find("rayEnd"), clanSlot)
            xml.addElement("rayUp", newClanSlot.find("rayUp"), clanSlot)
            xml.addElement("size", newClanSlot.find("size"), clanSlot)
            xml.addElement("hideIfDamaged", newClanSlot.find("hideIfDamaged"), clanSlot)
            xml.addElement("isUVProportional", newClanSlot.find("isUVProportional"), clanSlot)

        selectedChassis = tankXmlStorage[rand].find("chassis").find("*")
        thisChassis = root.find("chassis").findall("*")

        for c in thisChassis:
            xml.addElement("models", selectedChassis.find("models"), c)
            xml.addElement("AODecals", selectedChassis.find("AODecals"), c)
            xml.addElement("wwsoundPC", selectedChassis.find("wwsoundPC"), c)
            xml.addElement("wwsoundNPC", selectedChassis.find("wwsoundNPC"), c)
            xml.addElement("drivingWheels", selectedChassis.find("drivingWheels"), c)
            xml.addElement("trackNodes", selectedChassis.find("trackNodes"), c)
            xml.addElement("groundNodes", selectedChassis.find("groundNodes"), c)
            xml.addElement("splineDesc", selectedChassis.find("splineDesc"), c)
            xml.addElement("wheels", selectedChassis.find("wheels"), c)
            xml.addElement("trackThickness", selectedChassis.find("trackThickness"), c)
            xml.addElement("tracks", selectedChassis.find("tracks"), c)
            xml.addElement("traces", selectedChassis.find("traces"), c)
            xml.addElement("effects", selectedChassis.find("effects"), c)
            xml.addElement("physicalTracks", selectedChassis.find("physicalTracks"), c)
            
            if xml.elementExists("leveredSuspension", selectedChassis):
                xml.addElement("leveredSuspension", selectedChassis.find("leveredSuspension"), c)
            else:
                xml.removeAllElementsByName("leveredSuspension", c)


        hullModels.pop(rand)
        tankXmlStorage.pop(rand)

        rand = xml.getRandomListIndex(conf.getRandomExhaustEffects(), random)
        effect = conf.getRandomExhaustEffects()[rand]
        xml.insertElement("pixie", effect, root.find("hull").find("exhaust"))
    
    for t in root.find("turrets0").findall("*"):
        if randModels == "true":
            rand = xml.getRandomListIndex(turrets, random)
            randomModel = turrets[rand]
            xml.addElement("models", randomModel.find("models"), t)

            if xml.elementExists("ceilless", randomModel):
                xml.addElement("ceilless", randomModel.find("ceilless"), t)
            else:
                xml.insertElement("ceilless", "false", t)

            turrets.pop(rand)

        for g in t.find("guns").findall("*"):

            #gun effect is randomized twice (second time is in gunEffectRandomizer.py, this is required)

            isDoubleGun = g.find("RAND_IsDoubleGun").text.lower()

            if randModels == "true" and isDoubleGun == "false":
                rand = xml.getRandomListIndex(guns, random)
                randomModel = guns[rand]
                xml.addElement("models", randomModel.find("models"), g)
                xml.addElement("drivenJoints", randomModel.find("drivenJoints"), g)

                guns.pop(rand)

            if randGunFX == "true":

                #Do stuff if tank currently being randomized is NOT a double barreled vehicle
                if isDoubleGun == "false":
                    if seed == 666:
                        xml.insertElement("effects", "shot_superhuge", g)
                    else:
                        isDoubleGun_MODEL = randomModel.find("RAND_IsDoubleGun").text.lower()

                        if isDoubleGun_MODEL == "false":
                            efflist = conf.getRandomEffects()
                        else:
                            efflist = conf.getRandomDualGunEffects()

                        rand = xml.getRandomListIndex(efflist, random)
                        effect = efflist[rand]

                        xml.insertElement("effects", effect, g)

                #Do stuff if tank currently being randomized is a double barreled vehicle
                else:
                    
                    if seed == 666:
                        xml.insertElement("multiGunEffects", "shot_superhuge shot_superhuge", g)
                    else:
                        efflist = conf.getRandomDualGunEffects()

                        rand = xml.getRandomListIndex(efflist, random)
                        effect1 = efflist[rand]
                        rand = xml.getRandomListIndex(efflist, random)
                        effect2 = efflist[rand]

                        xml.insertElement("multiGunEffects", effect1 + " " + effect2, g)
            xml.removeAllElementsByName("RAND_IsDoubleGun", g)

    newtree = ET.ElementTree(root)

    newtree.write(tank.replace("Source", "Output"))

print("Starting randomization... please wait, this process might take a while.")
getFilePaths()

for t in tanks:
    getTankModels(t)

print("Stage 1... Done")

for t in tanks:
    updateTankModels(t)

print("Stage 2... Done")

print("\nTank Randomizing Complete")