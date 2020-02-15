import xml.etree.ElementTree as ET
import random

tree = ET.parse("Config/RandomizerConfig.xml")
root = tree.getroot()

seed = int(root.find("Seed").text)

if seed != 0:
    seedfile = open("Temp/seed.txt", 'w')
    seedfile.write(str(seed))
    seedfile.close()
else:
    seedfile = open("Temp/seed.txt", 'w')
    seed = random.randint(-2147483648, 2147483647)
    seedfile.write(str(seed))
    seedfile.close()