from configLoader import Config

import xml.etree.ElementTree as ET
import xmlMethods as xml
import random



def _remove_and_replace(name, new_element, where):
    xml.removeAllElementsByName(name, where)
    if new_element is not None:
        xml.replace_element(new_element.find(name), where)


class ShotEffectRandomizer:
    conf: Config

    pixies = []
    lights = []

    original_sounds = {}

    def __init__(self, seed: int, config: Config):
        random.seed(seed)
        self.conf = config

        self.tree = ET.parse(self.conf.shotEffectsPath)
        root = self.tree.getroot()
        self.effects = root.findall("*")

        for i in self.effects:
            for item in i.findall("*"):
                item_pixies = item.findall("effects")
                item_lights = item.findall("light")

                for j in item_pixies:
                    self.pixies.append(j)
                    sound = j.find("sound")
                    if sound is not None:
                        self.original_sounds[j] = sound
                for j in item_lights:
                    self.lights.append(j)

    def randomize(self):
        num = 0
        numMax = len(self.effects)

        for i in self.effects:
            num += 1

            percent = round(num / numMax * 100, 1)
            print(f"({percent}%) Randomizing effect: {i.tag}")

            for item in i.findall("*"):
                pixie = item.find("effects")
                light = item.find("light")

                if pixie is not None:
                    idx = xml.getRandomListIndex(self.pixies, random)
                    rand_pixie = self.pixies[idx]

                    try:
                        sound_old = self.original_sounds[pixie]
                        sound_new = self.original_sounds[rand_pixie]

                        if sound_old is not None and sound_new is not None:
                            xml.replace_element(sound_old, rand_pixie)
                            xml.replace_element(sound_new, pixie)
                    except Exception:
                        pass

                    xml.replace_element(rand_pixie, item)
                    self.pixies.pop(idx)

                if light is not None:
                    idx = xml.getRandomListIndex(self.lights, random)
                    rand_light = self.lights[idx]
                    xml.replace_element(rand_light, item)
                    self.lights.pop(idx)

    def save(self):
        self.tree.write(self.conf.shotEffectsPathOut)

