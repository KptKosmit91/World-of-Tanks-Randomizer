'''

WoT randomizer config controller written by KptKosmit91

PLEASE DO NOT MODIFY THIS FILE UNLESS YOU KNOW WHAT YOU'RE DOING!
For the true Config file see Config/RandomizerConfig.xml

'''

randomizerversion = "0.9.5"
wotversion="1.11.0"

resOut = "Output/res/"

mapsPath = "Source/res/scripts/arena_defs/"
mapsPathOut = "Output/res/scripts/arena_defs/"

itemDefsPath = "Source/res/scripts/item_defs/"
itemDefsPathOut = "Output/res/scripts/item_defs/"

tanksPath = "Source/res/scripts/item_defs/vehicles/"
tanksPathOut = "Output/res/scripts/item_defs/vehicles/"

addonNewTankModelsPath = "Addons/NewTankModels/"
addonNewTankModelsVehiclesPath = "Addons/NewTankModels/Source/res/scripts/item_defs/vehicles/"

# vehicle folders
countryFolders={
    "Ch": "china",
    "Cz": "czech",
    "F": "france",
    "G": "germany",
    "It": "italy",
    "J": "japan",
    "Pl": "poland",
    "S": "sweden",
    "GB": "uk",
    "A": "usa",
    "R": "ussr"
}
import os

if os.path.exists("Temp/seed.txt"):
    seed = open("Temp/seed.txt", 'r').read()
else:
    seed = 0

import xml.etree.ElementTree as ET

tree = ET.parse("Config/RandomizerConfig.xml")
root = tree.getroot()

wotmodName=root.find("WotmodFilename").text

tankrandomizer = root.find("TankRandomizer")

#toggles
chaosModeEnabled = tankrandomizer.find("ChaosModeEnabled").text.lower()

RandomizeTankModels = tankrandomizer.find("RandomizeTankModels").text.lower()

TankModelRandomizationIsUnique = tankrandomizer.find("TankModelRandomizationIsUnique").text.lower()

def renewTankModelIsUniqueSetting():
    TankModelRandomizationIsUnique = tankrandomizer.find("TankModelRandomizationIsUnique").text.lower()

__KeywordsText = ""
__KeywordsText = tankrandomizer.find("Keywords").text

KeywordsString = ""

if __KeywordsText is not None:
    KeywordsString = __KeywordsText.lower().replace(",", " ").replace(".", " ")

KeywordsArray = []
UseKeywords = "false"

if KeywordsString is not None and KeywordsString is not "":
    KeywordsArray = KeywordsString.split()
    UseKeywords = "true"
    TankModelRandomizationIsUnique = "false"

def hasKeyword(text):

    for keyword in KeywordsArray:
        if keyword.lower() in text.lower():
            return "true"

RandomizeEngineSounds = tankrandomizer.find("RandomizeEngineSounds").text.lower()
RandomizeGunEffectsAndSounds = tankrandomizer.find("RandomizeGunEffectsAndSounds").text.lower()
RandomizeEngineRPM = tankrandomizer.find("RandomizeEngineRPM").text.lower()
RandomizeMusicOnMaps = tankrandomizer.find("RandomizeMusicOnMaps").text.lower()
RandomizeCrewPrompts = tankrandomizer.find("RandomizeCrewPrompts").text.lower()
RandomizeShellImpactSounds = tankrandomizer.find("RandomizeShellImpactSounds").text.lower()
RandomizeTankPaints = tankrandomizer.find("RandomizeTankPaints").text.lower()

RandomizeMapNames = tankrandomizer.find("RandomizeMapNames").text.lower()
RandomizeMapNamesWithTankNames = tankrandomizer.find("RandomizeMapNamesWithTankNames").text.lower()

RandomizeFoliageColor = tankrandomizer.find("RandomizeFoliageColor").text.lower()

CustomSounds = tankrandomizer.find("CustomSounds").text.lower()
UseAlternativeGunSoundsMod = tankrandomizer.find("UseAlternativeGunSoundsMod").text.lower()
UseOldGunSoundsMod = tankrandomizer.find("UseOldGunSoundsMod").text.lower()
#end toggles

SensitivityToImpulseMin = float(tankrandomizer.find("SensitivityToImpulseMin").text)
SensitivityToImpulseMax = float(tankrandomizer.find("SensitivityToImpulseMax").text)

rpm_minMin = float(tankrandomizer.find("EngineRPM_Min").find("Min").text)
rpm_minMax = float(tankrandomizer.find("EngineRPM_Min").find("Max").text)
rpm_maxMin = float(tankrandomizer.find("EngineRPM_Max").find("Min").text)
rpm_maxMax = float(tankrandomizer.find("EngineRPM_Max").find("Max").text)

def isBlacklisted(tank):
    if tank.lower().endswith(".xml") == False:
        return True
    if tank.lower() == "customization.xml":
        return True
    if tank.lower() == "list.xml":
        return True
    if tank.lower().endswith("_igr.xml"):
        return True
    if tank.lower().endswith("_bot.xml"):
        return True
    if tank.lower().endswith("_test.xml"):
        return True

    tanks = tankrandomizer.find("ModelRandomizerBlacklist").findall("Tank")
    for t in tanks:
        if tank.lower() == (t.text +".xml").lower():
            return True

    return False

def getSpecialAttributesFor(tank):
    tanks = tankrandomizer.find("ModelRandomizerSpecialList").findall("Tank")
    for t in tanks:
        if tank == t.text +".xml":
            return t.attrib

    return None

def getRandomDualGunEffects():
    effects = tankrandomizer.find("DualGunEffectList").findall("Effect")
    l = []
    for e in effects:
        l.append(e.text)

        if UseAlternativeGunSoundsMod == "true":
            tree1 = ET.parse("Addons/AlternativeGunSounds/Config/RandomizerConfig.xml")
            root1 = tree1.getroot()

            random = root1.find("TankRandomizer")
            effects = random.find("DualGunEffectList").findall("Effect")
            for e in effects:
                l.append(e.text)

    return l

def getRandomEffects():
    effects = tankrandomizer.find("GunEffectList").findall("Effect")
    l = []
    for e in effects:
        l.append(e.text)

    if CustomSounds == "true":

        if UseAlternativeGunSoundsMod == "true":
            tree1 = ET.parse("Addons/AlternativeGunSounds/Config/RandomizerConfig.xml")
            root1 = tree1.getroot()

            random = root1.find("TankRandomizer")
            effects = random.find("GunEffectList").findall("Effect")
            for e in effects:
                l.append(e.text)

        if UseOldGunSoundsMod == "true":
            tree1 = ET.parse("Addons/OldGunSounds/Config/RandomizerConfig.xml")
            root1 = tree1.getroot()

            random = root1.find("TankRandomizer")
            effects = random.find("GunEffectList").findall("Effect")
            for e in effects:
                l.append(e.text)

    return l

def getRandomReloadEffects():
    effects = tankrandomizer.find("GunReloadSFXList").findall("Effect")
    l = []
    for e in effects:
        l.append(e.text)

    return l

def getRandomRecoilEffects():
    effects = tankrandomizer.find("GunRecoilEffectsList").findall("Effect")
    l = []
    for e in effects:
        l.append(e.text)

    return l

def getRandomExhaustEffects():
    effects = tankrandomizer.find("ExhaustEffectList").findall("Effect")
    l = []
    for e in effects:
        l.append(e.text)

    return l

def getEngineSFX(etype):
    if etype.lower() == "npc":
        effects = tankrandomizer.find("EngineSFXList").find("NPC").findall("WWEvent")
    if etype.lower() == "pc":
        effects = tankrandomizer.find("EngineSFXList").find("PC").findall("WWEvent")

    l = []
    for e in effects:
        l.append(e.text)

    return l