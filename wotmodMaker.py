'''

WoT randomizer - wotmod packer written by KptKosmit91
Packs Output/res into a .wotmod file

'''

from zipfile import ZipFile
import config as conf
import os
from time import sleep

name = conf.wotmodName.replace("$randver", conf.randomizerversion).replace("$wotver", conf.wotversion).replace("$seed", conf.seed)
wotmod = ZipFile('Output/' + name + '.wotmod', 'w')

print("Packing mod...")

for folderName, subfolders, filenames in os.walk(conf.resOut):
    for filename in filenames:
        #create complete filepath of file in directory
        filePath = os.path.join(folderName, filename)
        # Add file to zip
        wotmod.write(filePath, arcname=filePath.replace("Output/", ""), compress_type=None, compresslevel=None)

# wotmod.write("Source/res/vehicles", arcname="res/vehicles", compress_type=None, compresslevel=None)
# wotmod.write("Addons/NewTankModels/Source/res/vehicles", arcname="res/vehicles", compress_type=None, compresslevel=None )
# wotmod.write("Addons/NewTankModels/Source/res/FiatBojowy", arcname="res/FiatBojowy", compress_type=None, compresslevel=None)

from shutil import rmtree
if os.path.exists("Temp"):
    rmtree("Temp")

if os.path.exists(conf.resOut):
    rmtree(conf.resOut)

print("Packing done!\nYou are ready to install your mod!")

sleep(2)