from typing import Dict, Any

from configLoader import Config
import os
import xml.etree.ElementTree as ET


class Guns:
    conf: Config = None

    gunsFilePaths = []
    rootDict: dict[str, ET.Element] = {}
    gunDict: dict[str, ET.Element] = {}

    def __init__(self, config):
        self.conf = config

    def gather_information(self):
        for f in self.conf.countryFolders:
            folder = self.conf.tanksPath + self.conf.countryFolders[f] + "/components/"
            if os.path.exists(folder):
                for n in os.listdir(folder):
                    if "guns.xml" in n:
                        #print("Found guns.xml: " + folder + n)
                        self.gunsFilePaths.append(folder + n)

        for path in self.gunsFilePaths:
            tree = ET.parse(path)
            root = tree.getroot()

            self.rootDict[path] = root

            shared = root.find("shared")
            all_guns = shared.findall("*")

            for gun in all_guns:
                name = gun.tag
                self.gunDict[name] = gun
                # print(f"Added gun {name}: {gun}")

    def getGun(self, name: str) -> ET.Element:
        if name in self.gunDict:
            return self.gunDict[name]
        else:
            # print(f"Could not find gun {name} !")
            return None


