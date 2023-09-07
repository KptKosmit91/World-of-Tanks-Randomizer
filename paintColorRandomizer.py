import xml.etree.ElementTree as ET
import xmlMethods as xml
from configLoader import Config
import random
import fileMethods as fm
from os import path


class PaintRandomizer:
    conf: Config = None

    def __init__(self, seed, conf):
        random.seed(seed)
        self.conf = conf

    def randomize(self):
        if path.exists(self.conf.itemDefsPath + "customization/paints/list.xml") == False:
            print("Could not find paints list.xml file.")
            return

        tree = ET.parse(self.conf.itemDefsPath + "customization/paints/list.xml")
        root = tree.getroot()

        itemGroups = root.findall("itemGroup")

        num = 0
        num_max = len(itemGroups)

        for itemGroup in itemGroups:
            num += 1

            percent = round(num / num_max * 100, 1)
            print(f"({percent}%) Randomizing paint group: {itemGroup.find('userString').text}")

            for paint in itemGroup.findall("paint"):
                xml.insertElement("color", str(self.get_random_color()) + " " + str(self.get_random_color()) + " " + str(self.get_random_color()) + " " + "255", paint)
                xml.insertElement("gloss", str(random.uniform(0, 1)), paint)
                xml.insertElement("metallic", str(random.uniform(0, 1)), paint)

        fm.createFolder(self.conf.itemDefsPathOut + "customization/paints")
        tree.write(self.conf.itemDefsPathOut + "customization/paints/list.xml")

    def get_random_color(self):
        return random.randint(0, 255 * 2) % 255
