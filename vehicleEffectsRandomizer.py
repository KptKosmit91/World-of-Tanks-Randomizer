from configLoader import Config

import xml.etree.ElementTree as ET
import xmlMethods as xml
import random

class VehicleEffectRandomizer:
    conf: Config

    explEffects = []
    explNames = []

    def isValidExplosion(self, tag):
        return "trackdestruction" not in tag and "empty" not in tag and ("explosion" in tag or "destruction" in tag or "crewdeath" in tag or "submersiondeath" in tag)

    def __init__(self, seed: int, config: Config):
        random.seed(seed)
        self.conf = config

        self.tree = ET.parse(self.conf.vehEffectsPath)
        root = self.tree.getroot()
        effects = root.findall("*")

        for item in effects:
            if self.isValidExplosion(item.tag.lower()):
                self.explEffects.append(item)
                self.explNames.append(item.tag)

    def randomize(self):
        num = 0
        num_max = len(self.explEffects)

        for e in self.explEffects:
            num += 1

            percent = round(num / num_max * 100, 1)
            print(f"({percent}%) Randomizing vehicle effect: {e.tag}")

            idx = xml.getRandomListIndex(self.explNames, random)
            e.tag = self.explNames[idx]
            self.explNames.pop(idx)

    def save(self):
        self.tree.write(self.conf.vehEffectsPathOut)