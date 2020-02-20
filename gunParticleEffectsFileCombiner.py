import os
import config as conf
import fileMethods as fm

header = "<gun_effects.xml>"
footer = "</gun_effects.xml>"

files = []

if conf.CustomSounds == "false":
    quit()


files.append(conf.tanksPath + "common/gun_effects.xml")

files.append("Addons/NewGunEffects/Source/res/scripts/item_defs/vehicles/common/gun_effects.xml")

if conf.UseAlternativeGunSoundsMod == "true":
    files.append("Addons/AlternativeGunSounds/Source/res/scripts/item_defs/vehicles/common/gun_effects.xml")

if conf.UseOldGunSoundsMod == "true":
    files.append("Addons/OldGunSounds/Source/res/scripts/item_defs/vehicles/common/gun_effects.xml")

if len(files) <= 1:
    quit()

fm.createFolder(conf.tanksPathOut + "common/")
outputFile = open(conf.tanksPathOut + "common/gun_effects.xml", 'w')
outputFile.write(header)

for f in files:
    gun_effects = open(f, 'r')
    text = gun_effects.read()
    text = text.replace(header, "").replace(footer, "")

    outputFile.write(text)

    gun_effects.close()

outputFile.write(footer)

outputFile.close()