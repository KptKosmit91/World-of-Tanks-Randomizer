import config as conf
from time import sleep
from shutil import rmtree
from distutils.dir_util import copy_tree as copytree
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
if os.path.exists("Output/res/vehicles"):
    rmtree("Output/res/vehicles")

for f in conf.countryFolders:
    folder = conf.tanksPathOut+conf.countryFolders[f]
    fm.createFolder(folder+"/components")

fm.createFolder(conf.mapsPathOut)
fm.createFolder("Output/res/spaces")

printSetting("Chaos Mode Enabled", conf.chaosModeEnabled)
printSetting("Randomize Tank Models", conf.RandomizeTankModels)
printSetting("Use Keywords for Tank Models", conf.UseKeywords)
if conf.UseKeywords == "true":
    printSetting(" " + str(len(conf.KeywordsArray)) + " Keyword(s) used", str(conf.KeywordsArray))
printSetting("Tank Model Randomization Is Unique", conf.TankModelRandomizationIsUnique)
printSetting("Randomize Gun Effects And Sounds", conf.RandomizeGunEffectsAndSounds)
printSetting("Randomize Engine Sounds", conf.RandomizeEngineSounds)
printSetting("Randomize Engine RPM", conf.RandomizeEngineRPM)
printSetting("Randomize Music On Maps", conf.RandomizeMusicOnMaps)
printSetting("Randomize Crew Prompts", conf.RandomizeCrewPrompts)
printSetting("Randomize Shell Impact Sounds", conf.RandomizeShellImpactSounds)
printSetting("Custom Sounds", conf.CustomSounds)
printSetting("Use Alternative Gun Sounds", conf.UseAlternativeGunSoundsMod)
printSetting("Use Old Gun Sounds", conf.UseOldGunSoundsMod)

print("\nCopying additional tank model files... Don't worry if the window is stuck or frozen.\n")

copytree("Source/res/vehicles", "Output/res/vehicles")
copytree("Addons/NewTankModels/Source/res/vehicles", "Output/res/vehicles")
copytree("Addons/NewTankModels/Source/res/FiatBojowy", "Output/res/FiatBojowy")

copytree("SourceOverrides/res/scripts/item_defs/vehicles", "Source/res/scripts/item_defs/vehicles")

print("\nCopying completed!\n")
