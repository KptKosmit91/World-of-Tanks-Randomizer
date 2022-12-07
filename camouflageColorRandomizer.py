import xml.etree.ElementTree as ET
import xmlMethods as xml
from configLoader import Config
import random
import fileMethods as fm
from os import path


class CamouflageRandomizer:
    conf: Config = None

    def __init__(self, seed, conf):
        random.seed(seed)
        self.conf = conf

    def randomize(self):
        if path.exists(self.conf.itemDefsPath + "customization/camouflages/list.xml") == False:
            print("Could not find camouflage list.xml file.")
            return

        tree = ET.parse(self.conf.itemDefsPath + "customization/camouflages/list.xml")
        root = tree.getroot()

        itemGroups = root.findall("itemGroup");

        num = 0
        num_max = len(itemGroups)

        for itemGroup in itemGroups:
            num += 1

            percent = round(num / num_max * 100, 1)
            print(f"({percent}%) Randomizing camouflages")

            for camo in itemGroup.findall("camouflage"):
                for palette in camo.find("palettes").findall("palette"):
                    for colorData in palette.findall("*"):
                        if colorData.text.replace(" ", "").endswith("0"):
                            colorData.text = f"{self.get_random_color()} {self.get_random_color()} {self.get_random_color()} 0"
                        else:
                            colorData.text = f"{self.get_random_color()} {self.get_random_color()} {self.get_random_color()} 255"

        fm.createFolder(self.conf.itemDefsPathOut + "customization/camouflages")
        tree.write(self.conf.itemDefsPathOut + "customization/camouflages/list.xml")

    def get_random_color(self):
        return random.randint(0, 255 * 2) % 255
