from tankRandomizer import TankRandomizer
from shellEffectsRandomizer import ShotEffectRandomizer
from vehicleEffectsRandomizer import VehicleEffectRandomizer
from audiowwManager import AudiowwManager
from componentsxml import Guns
from configLoader import Config as conf
from configLoader import ConfigLoader
from gunEffectsCombiner import GunEffectsCombiner
import random
import os
from shutil import rmtree, copytree
from distutils.dir_util import copy_tree, create_tree
from wotmodMaker import WotmodMaker

from time import sleep

import threading


def setup_output_folder():
    print("Preparing output folder")

    threads = []

    if os.path.exists(conf.resPathOut):
        for folder in os.listdir(conf.resPathOut):
            t = threading.Thread(target=threaded_remove, args=[conf.resPathOut + folder])
            t.start()
            threads.append(t)

    for thread in threads:
        thread.join()

    os.makedirs(conf.audiowwPathOut)

    for f in conf.countryFolders:
        os.makedirs("Output/res/scripts/item_defs/vehicles/" + conf.countryFolders[f])

    # common directory
    os.makedirs("Output/res/scripts/item_defs/vehicles/common")

    print("Output folder ready!\n")


def threaded_remove(source):
    if os.path.isdir(source):
        rmtree(source)
    else:
        os.remove(source)


def threaded_copytree(source, output):
    copytree(source, output)


def symlink(inp, outp):
    if not os.path.exists(inp):
        print(f"Failed to create symlink: input path {inp} does not exist.")
        return None
    #if not os.path.exists(outp):
        #os.makedirs(outp, True)

    os.symlink(os.path.abspath(inp), os.path.abspath(outp))


def main():
    ConfigLoader.load_config()

    if conf.seed == 0:
        seed = random.randrange(-2147483648, 2147483647)
    else:
        seed = conf.seed
    # seed = 354658851

    print("\nRandomizer seed: " + str(seed))

    sleep(0.5)

    setup_output_folder()

    audioww = AudiowwManager(conf, seed)
    audioww.gather_information()

    gun_effects_combiner = GunEffectsCombiner(conf)
    gun_effects_combiner.gather_information()
    gun_effects_combiner.combine()

    guns = Guns(conf)
    guns.gather_information()


    print("Tank Randomizer")
    tank_randomizer = TankRandomizer(seed, conf, guns)

    print("Gathering tank information...")
    tank_randomizer.gather_information()

    tank_randomizer.get_tank_models()
    print("Information gathered")

    print("Randomizing tank models")
    tank_randomizer.randomize()

    # print("Shell Effect Randomizer")
    # effect_randomizer = ShotEffectRandomizer(seed, conf)
    #
    # print("Randomizing shell effects...")
    # effect_randomizer.randomize()
    #
    # effect_randomizer.save()
    # print("Randomizing shell effects complete")

    print("\nVehicle Effect Randomizer")
    vehicle_randomizer = VehicleEffectRandomizer(seed, conf)

    print("Randomizing vehicle effects...")
    vehicle_randomizer.randomize()

    vehicle_randomizer.save()
    print("Randomizing vehicle effects complete")


    audioww.create_audiomodsxml()

    print("\nCopying required mod files to Output")

    thread_list = []

    for country in conf.vehicleModelsCountryFolders.values():
        for addon in conf.activeAddons:
            vehicles_addon_path = f"{addon}res/vehicles/{country}"
            if os.path.exists(vehicles_addon_path):
                # symlink(vehicles_addon_path, f"Output/res/vehicles/{country}")

                t = threading.Thread(target=threaded_copytree, args=[vehicles_addon_path, f"Output/res/vehicles/{country}"])
                t.start()
                thread_list.append(t)

                # copytree(vehicles_addon_path, f"Output/res/vehicles/{country}")

            if "/NewTankModels/" in addon and country == "poland":
                # symlink(f"{addon}res/FiatBojowy", "Output/res/FiatBojowy")

                t = threading.Thread(target=threaded_copytree, args=[f"{addon}res/FiatBojowy", "Output/res/FiatBojowy"])
                t.start()
                thread_list.append(t)

                # copytree(f"{addon}res/FiatBojowy", "Output/res/FiatBojowy")

    for thread in thread_list:
        thread.join()

    print("Copying done!")

    print("\nPacking mod, please wait... This process might take a while.")
    try:
        wotmod = WotmodMaker(conf, seed)
        wotmod.create_wotmod()

        print("Mod packing finished!")
    except Exception as e:
        print("\nAn error occurred while trying to create the wotmod file!")
        print(str(e))


if __name__ == "__main__":
    main()
