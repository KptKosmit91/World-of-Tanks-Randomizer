from configLoader import Config

import xml.etree.ElementTree as ET
import xmlMethods as xml
import random

from copy import deepcopy



def _remove_and_replace(name, new_element, where):
    xml.removeAllElementsByName(name, where)
    if new_element is not None:
        xml.replace_element(new_element.find(name), where)


class ShotEffectRandomizer:
    conf: Config

    pixies = []
    lights = []

    original_sounds = {}

    def isProhibitedTag(self, tag: str):
        return tag.startswith("projectile")

    def __init__(self, seed: int, config: Config):
        random.seed(seed)
        self.conf = config

        self.tree = ET.parse(self.conf.shotEffectsPath)
        root = self.tree.getroot()
        self.effects = root.findall("*")

        for i in self.effects:
            for item in i.findall("*"):

                if self.isProhibitedTag(item.tag):
                    continue

                item_pixies = deepcopy(item.findall("effects"))

                for j in item_pixies:
                    self.pixies.append(j)
                    sound = j.find("sound")
                    if sound is not None:
                        self.original_sounds[j] = sound

    def randomize(self):
        num = 0
        numMax = len(self.effects)

        for i in self.effects:
            num += 1

            percent = round(num / numMax * 100, 1)
            print(f"({percent}%) Randomizing effect: {i.tag}")


            for item in i.findall("*"):

                if item.tag == "targetImpulse":
                    targetImpulseValue = random.uniform(0.01, 5)
                    item.text = str(targetImpulseValue)
                    continue

                if item.tag == "waterParams":
                    elem = item.find("shallowWaterDepth")
                    elem.text = str(random.uniform(0.75, 1.5))
                    elem = item.find("rippleDiameter")
                    elem.text = str(random.uniform(0.3, 5))
                    continue

                if item.tag == "physicsParams":
                    elem = item.find("splashRadius")
                    elem.text = str(random.uniform(0.1, 75))
                    elem = item.find("splashStrength")
                    elem.text = str(random.uniform(0.1, 50))
                    continue

                if self.isProhibitedTag(item.tag):
                    continue

                # print(f"     SECTION NAME: {item.tag}")

                pixie = item.find("effects")

                if pixie is not None:
                    idx = xml.getRandomListIndex(self.pixies, random)
                    rand_pixie = self.pixies[idx]

                    # try:
                    #     sound_old = self.original_sounds[pixie]
                    #     sound_new = self.original_sounds[rand_pixie]
                    #
                    #     if sound_old is not None and sound_new is not None:
                    #         xml.replace_element(sound_old, rand_pixie)
                    #         xml.replace_element(sound_new, pixie)
                    # except Exception:
                    #     pass

                    xml.replace_element(rand_pixie, item)
                    self.pixies.pop(idx)

    def save(self):
        self.tree.write(self.conf.shotEffectsPathOut)

