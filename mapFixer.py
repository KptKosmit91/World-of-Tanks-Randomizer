import xml.etree.ElementTree as ET
import xmlMethods as xml
import config as conf
import os
import fileMethods as fm


maps = []

def loadMaps():
    folder = conf.mapsPath
    for n in os.listdir(folder):
        if n.lower() != "_default_.xml" and n.lower() != "_list_.xml" and n.lower() != "hangar_v3.xml" and n.lower() != "1002_ai_test.xml":
            maps.append(folder+n)

loadMaps()

for m in maps:
    f = open(m, "r")
    mapName = m.replace(conf.mapsPath, "")
    text=f.read()
    text = text.replace(mapName,"root")

    f.close()

    f = open(m, "w")
    f.write(text)
    f.close()