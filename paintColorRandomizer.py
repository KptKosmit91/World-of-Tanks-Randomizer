import xml.etree.ElementTree as ET
import xmlMethods as xml
import config as conf
import os
import random
import fileMethods as fm
from shutil import copyfile

if conf.RandomizeTankPaints != "true":
    print("Paint color randomization is disabled, skipping.")
    quit()

tree = ET.parse(conf.itemDefsPath + "customization/paints/list.xml")
root = tree.getroot()

random.seed = conf.seed

for itemGroup in root.findall("itemGroup"):
    for paint in itemGroup.findall("paint"):
        xml.insertElement("color", str(random.randint(0, 255)) + " " + str(random.randint(0, 255)) + " " + str(random.randint(0, 255)) + " " + "255", paint)
        xml.insertElement("gloss", str(random.uniform(0, 1)), paint)
        xml.insertElement("metallic", str(random.uniform(0, 1)), paint)

fm.createFolder(conf.itemDefsPathOut + "customization/paints")
newtree = ET.ElementTree(root)
newtree.write(conf.itemDefsPathOut + "customization/paints/list.xml")

print("Paint color randomization completed successfully.")