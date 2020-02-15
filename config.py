randomizerversion = "0.7"
wotversion="1.7.1"

resOut = "Output/res/"

mapsPath = "Source/res/scripts/arena_defs/"
mapsPathOut = "Output/res/scripts/arena_defs/"

tanksPath = "Source/res/scripts/item_defs/vehicles/"
tanksPathOut = "Output/res/scripts/item_defs/vehicles/"

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
seed = open("Temp/seed.txt", 'r').read()

import xml.etree.ElementTree as ET

tree = ET.parse("Config/RandomizerConfig.xml")
root = tree.getroot()

wotmodName=root.find("WotmodFilename").text

tankrandomizer = root.find("TankRandomizer")

#Toggles
chaosModeEnabled = tankrandomizer.find("ChaosModeEnabled").text.lower()
RandomizeTankModels = tankrandomizer.find("RandomizeTankModels").text.lower()
RandomizeEngineSounds = tankrandomizer.find("RandomizeEngineSounds").text.lower()
RandomizeGunEffectsAndSounds = tankrandomizer.find("RandomizeGunEffectsAndSounds").text.lower()
RandomizeEngineRPM = tankrandomizer.find("RandomizeEngineRPM").text.lower()
RandomizeMusicOnMaps = tankrandomizer.find("RandomizeMusicOnMaps").text.lower()
RandomizeCrewPrompts = tankrandomizer.find("RandomizeCrewPrompts").text.lower()
RandomizeShellImpactSounds = tankrandomizer.find("RandomizeShellImpactSounds").text.lower()
CustomSounds = tankrandomizer.find("CustomSounds").text.lower()

RandomizeMapNames = tankrandomizer.find("RandomizeMapNames").text.lower()
RandomizeMapNamesWithTankNames = tankrandomizer.find("RandomizeMapNamesWithTankNames").text.lower()

RandomizeFoliageColor = tankrandomizer.find("RandomizeFoliageColor").text.lower()

SensitivityToImpulseMin = float(tankrandomizer.find("SensitivityToImpulseMin").text)
SensitivityToImpulseMax = float(tankrandomizer.find("SensitivityToImpulseMax").text)

rpm_minMin = float(tankrandomizer.find("EngineRPM_Min").find("Min").text)
rpm_minMax = float(tankrandomizer.find("EngineRPM_Min").find("Max").text)
rpm_maxMin = float(tankrandomizer.find("EngineRPM_Max").find("Min").text)
rpm_maxMax = float(tankrandomizer.find("EngineRPM_Max").find("Max").text)

def isBlacklisted(tank):
    if tank.endswith("_IGR.xml"):
        return True

    tanks = tankrandomizer.find("ModelRandomizerBlacklist").findall("Tank")
    for t in tanks:
        if tank == t.text +".xml":
            return True

    return False

def getSpecialAttributesFor(tank):
    tanks = tankrandomizer.find("ModelRandomizerSpecialList").findall("Tank")
    for t in tanks:
        if tank == t.text +".xml":
            return t.attrib

    return None

def getRandomEffects():
    effects = tankrandomizer.find("GunEffectList").findall("Effect")
    l = []
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