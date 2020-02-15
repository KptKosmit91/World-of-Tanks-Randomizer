import config as conf
from shutil import rmtree
import os
import fileMethods as fm
import config as conf

def printSetting(text, setting):
    print(text + ": " + setting)

if os.path.exists("Output/res/audioww"):
    rmtree("Output/res/audioww")
if os.path.exists("Output/res/scripts"):
    rmtree("Output/res/scripts")
if os.path.exists("Output/res/spaces"):
    rmtree("Output/res/spaces")

for f in conf.countryFolders:
    folder = conf.tanksPathOut+conf.countryFolders[f]
    fm.createFolder(folder+"/components")

fm.createFolder(conf.mapsPathOut)
fm.createFolder("Output/res/spaces")

printSetting("Chaos Mode Enabled", conf.chaosModeEnabled)
printSetting("Randomize Tank Models", conf.RandomizeTankModels)
printSetting("Randomize Gun Effects And Sounds", conf.RandomizeGunEffectsAndSounds)
printSetting("Randomize Engine Sounds", conf.RandomizeEngineSounds)
printSetting("Randomize Engine RPM", conf.RandomizeEngineRPM)
printSetting("Randomize Music OnMaps", conf.RandomizeMusicOnMaps)
printSetting("Randomize Crew Prompts", conf.RandomizeCrewPrompts)
printSetting("Randomize Shell Impact Sounds", conf.RandomizeShellImpactSounds)
printSetting("Custom Sounds", conf.CustomSounds)