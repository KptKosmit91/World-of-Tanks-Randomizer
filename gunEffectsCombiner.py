import os
from configLoader import Config
from shutil import copyfile

import xml.etree.ElementTree as ET


class GunEffectsCombiner:
    conf: Config = None

    def __init__(self, config: Config):
        self.conf = config

    effectFiles = []

    def gather_information(self):
        folder = self.conf.tanksPath + "common/"
        if os.path.exists(folder):
            for file_name in os.listdir(folder):
                if "gun_effects" in file_name:
                    self.effectFiles.append(folder + file_name)

        for addon in self.conf.activeAddons:
            folder = self.conf.tanksPath.replace("Source/", addon) + "common/"
            if os.path.exists(folder):
                for file_name in os.listdir(folder):
                    if "gun_effects" in file_name:
                        self.effectFiles.append(folder + file_name)

    def combine(self):
        length = len(self.effectFiles)
        if length == 0:
            return None

        write_path = self.conf.tanksPathOut + "common/gun_effects.xml"
        if length == 1:
            copyfile(self.effectFiles[0], write_path)
            return None

        new_effects = []

        original_file = self.effectFiles[0]
        self.effectFiles.pop(0)
        original_tree = ET.parse(original_file)
        original_root = original_tree.getroot()

        for filepath in self.effectFiles:
            tree = ET.parse(filepath)
            root = tree.getroot()

            for effect in root.findall("*"):
                original_root.append(effect)

        for effect in original_root.findall("*"):
            effect_name = effect.tag
            if "dual" in effect_name.lower() and "single" not in effect_name.lower():
                # print("Dual Effect: " + effect.tag)
                self.conf.gunEffectsDual.append(effect.tag)
            else:
                # print("Effect: " + effect.tag)
                self.conf.gunEffects.append(effect.tag)

        original_tree.write(write_path)




        # for file in self.effectFiles:
