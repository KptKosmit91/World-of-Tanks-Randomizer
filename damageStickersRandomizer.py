from configLoader import Config

import xml.etree.ElementTree as ET
import xmlMethods as xml
import random


class DamageStickersRandomizer:
    conf: Config

    effects = []

    def __init__(self, seed: int, config: Config):
        random.seed(seed)
        self.conf = config

        self.tree = ET.parse(self.conf.dmgStickersPath)
        root = self.tree.getroot()
        self.effects = root.findall("*")

    def randomize(self):
        num = 0
        num_max = len(self.effects)

        for definition in self.effects:
            num += 1

            percent = round(num / num_max * 100, 1)
            print(f"({percent}%) Randomizing damage decal: {definition.tag}")

            for variant in definition.findall("*"):
                if not variant.tag.startswith("variant"):
                    continue

                scale1 = random.uniform(0.1, 4)
                scale2 = scale1 + random.uniform(-0.1, 0.1)

                if scale2 <= 0.02:
                    scale2 = 0.02

                variation = random.uniform(0.1, 0.5)

                element = variant.find("modelSizes")
                element.text = f"{scale1} {scale2}"

                element = variant.find("variation")
                element.text = f"{variation}"


    def save(self):
        self.tree.write(self.conf.dmgStickersPathOut)