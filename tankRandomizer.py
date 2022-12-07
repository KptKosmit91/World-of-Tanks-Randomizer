import time

from componentsxml import Guns
from xml.etree.ElementTree import Element, ElementTree

from configLoader import Config
import configLoader

import os
import xml.etree.ElementTree as ET
import xmlMethods as xml
import random

from time import sleep

import util

from copy import deepcopy

import threading


class Tank:

    gunList: list[Element] = []
    turretList: list[Element] = []
    chassisList: list[Element] = []
    hull: Element
    root: Element
    tree: ElementTree
    path: str

    def __init__(self, xmltree: ET.ElementTree, path: str, tank_randomizer, is_wheeled: bool):
        root = xmltree.getroot()

        self.tankRandomizer = tank_randomizer
        self.isWheeledVehicle = is_wheeled
        self.path = path

        self.tree = xmltree
        self.root = root

        self.hull = root.find("hull")
        self.chassisList = root.find("chassis").findall("*")
        self.turretList = root.find("turrets0").findall("*")
        self.gunList = []
        for turret in self.turretList:
            for gun in turret.find("guns").findall("*"):
                self.gunList.append(gun)

        add_to_randomizer_list = False

        if len(tank_randomizer.conf.keywords) == 0:
            add_to_randomizer_list = True
        else:
            for keyword in tank_randomizer.conf.keywords:
                if keyword.lower() in str(path).lower():
                    add_to_randomizer_list = True
                    break

        if add_to_randomizer_list and not is_wheeled:
            TankRandomizer.tankRootXmlList.append(deepcopy(root))
            TankRandomizer.tankHullList.append(deepcopy(self.hull))

            for chassis in self.chassisList:
                TankRandomizer.tankChassisList.append(deepcopy(chassis))

            for turret in self.turretList:
                TankRandomizer.tankTurretList.append(deepcopy(turret))

            for gun in self.gunList:
                TankRandomizer.tankGunList.append(deepcopy(gun))

            # TankRandomizer.tankChassisList = [deepcopy(obj) for obj in self.chassisList]
            # TankRandomizer.tankTurretList = [deepcopy(obj) for obj in self.turretList]
            # TankRandomizer.tankGunList = [deepcopy(obj) for obj in self.gunList]

            # print("---- TANK " + root.tag)
            # print("Hull: " + self.hull.tag)
            # for obj in self.chassisList:
            #     print("Chassis: " + obj.tag)
            # for obj in self.turretList:
            #     print("Turret: " + obj.tag)
            # for obj in self.gunList:
            #     print("Gun: " + obj.tag)


def _remove_and_replace(name, new_element, where):
    xml.removeAllElementsByName(name, where)
    if new_element is not None:
        xml.replace_element(new_element.find(name), where)


class TankRandomizer:
    conf: Config

    tankRootXmlList: list[Element] = []
    tankHullList: list[Element] = []
    tankChassisList: list[Element] = []
    tankTurretList: list[Element] = []
    tankGunList: list[Element] = []

    tanks: list[Tank] = []
    tankFilePaths = []

    guns: Guns = None

    def __init__(self, seed: int, config: Config, guns: Guns):
        random.seed(seed)
        self.conf = config
        self.guns = guns

    def gather_information(self):
        for f in self.conf.countryFolders:
            folder = self.conf.tanksPath + self.conf.countryFolders[f] + "/"
            if os.path.exists(folder):
                for n in os.listdir(folder):
                    if not self.conf.is_tank_blacklisted(n):
                        # print("Found tank: " + n)
                        self.tankFilePaths.append(folder + n)

            for addon in self.conf.activeAddons:
                folder = self.conf.tanksPath.replace("Source/", addon) + self.conf.countryFolders[f] + "/"
                if os.path.exists(folder):
                    for n in os.listdir(folder):
                        if not self.conf.is_tank_blacklisted(n):
                            # print("Found addon tank: " + folder + n)
                            self.tankFilePaths.append(folder + n)

    def threaded_get_tank_models(self, chunk_list):
        for tank in chunk_list:
            tree = ET.parse(tank)
            root = tree.getroot()

            # wheeled = root.find(xml.IsWheeledTag).text.lower()
            wheeled = configLoader.parse_bool(xml.IsWheeledTag, root, False)
            supported = True
            reason = ""

            if self.conf.fullTankRandomizer and wheeled:
                supported = False
                reason = "Wheeled vehicles are not supported with TankSwap=true"

            if supported:
                self.tanks.append(Tank(tree, tank, self, wheeled))
            else:
                print("Skipped vehicle: " + str(tank) + " Reason: " + reason)

    def get_tank_models(self):

        chunks = util.chunks(self.tankFilePaths, int(len(self.tankFilePaths) / 7))

        # threads = []

        for chunk in chunks:
            self.threaded_get_tank_models(chunk)

            # THREADING TEMPORARILY DISABLED
            # it currently might be breaking tank chassis if RandomizeChassisSeparately is set to false !

        #     t = threading.Thread(target=self.threaded_get_tank_models, args=[chunk])
        #     t.start()
        #     threads.append(t)
        #
        # for thread in threads:
        #     thread.join()

    def copyEmblemData(self, old, new):
        try:
            old.find("rayStart").text = new.find("rayStart").text
            old.find("rayEnd").text = new.find("rayEnd").text
            old.find("rayUp").text = new.find("rayUp").text
            old.find("size").text = new.find("size").text
            old.find("hideIfDamaged").text = new.find("hideIfDamaged").text
            old.find("isUVProportional").text = new.find("isUVProportional").text
        except:
            pass

    def copyProjectionDecalData(self, old, new):
        try:
            old.find("position").text = new.find("position").text
            old.find("rotation").text = new.find("rotation").text
            old.find("scale").text = new.find("scale").text
            old.find("doubleSided").text = new.find("doubleSided").text
            old.find("clipAngle").text = new.find("clipAngle").text
            old.find("anchorShift").text = new.find("anchorShift").text
        except:
            pass

    # i'm not entirely proud of the code here..
    def copy_customization(self, fromComp: Element, toComp: Element):
        slots_container_from = fromComp.find("customizationSlots")
        slots_container_to = toComp.find("customizationSlots")

        if slots_container_from is None or slots_container_to is None:
            return None

        clanEmblemNew = None
        clanEmblemOld = None

        for fromS in slots_container_from.findall("*"):
            for toS in slots_container_to.findall("*"):

                typeFrom = fromS.find("slotType").text
                typeTo = toS.find("slotType").text
                idFrom = fromS.find("slotId").text
                idTo = toS.find("slotId").text

                # print(f"Slot Type: {typeFrom} vs {typeTo}")

                if idFrom == idTo and typeFrom == typeTo:
                    if typeFrom == "player" or typeFrom == "inscription":
                        self.copyEmblemData(typeTo, typeFrom)
                    elif typeFrom == "projectionDecal":
                        self.copyProjectionDecalData(typeTo, typeFrom)



        for slot in slots_container_from.findall("*"):
            type = slot.find("slotType")
            if type == "clan":
                clanEmblemNew = slot

        for slot in slots_container_to.findall("*"):
            type = slot.find("slotType")
            if type == "clan":
                clanEmblemOld = slot

        if clanEmblemNew is not None and clanEmblemOld is not None:
            self.copyEmblemData(clanEmblemOld, clanEmblemNew)

        elif clanEmblemNew is not None:
            slots_container_to.append(clanEmblemNew)

        # xml.replace_element(toCustom, toComp)

    def randomize(self):
        iterate_tanks = [t for t in self.tanks if self.conf.addonsPath not in str(t.path)]

        count = len(iterate_tanks)
        current_tank = 0

        for tank in iterate_tanks:
            current_tank += 1
            percent = round(current_tank / count * 100, 1)

            print(f"({percent}%) Randomizing tank: {str(tank.path)}")

            chassis_count = len(tank.chassisList)
            turret_count = len(tank.turretList)
            gun_count = len(tank.gunList)

            # print("chassis count: " + str(chassis_count))
            # print("turret_count: " + str(turret_count))
            # print("gun_count: " + str(gun_count))

            random_hull_index = random.randrange(0, len(self.tankHullList))
            random_hull = self.tankHullList[random_hull_index]

            # self.copy_customization(random_hull, tank.hull)

            random_chassis_list = []
            random_turret_list = []
            random_gun_list = []

            hull_chassis = None

            if not self.conf.randomizeChassisSeparately:
                hull_chassis = self.tankRootXmlList[random_hull_index].find("chassis").find("*")

            should_pop_elements = self.conf.tankRandomizationIsUnique
            randomize_chassis = self.conf.randomizeChassis
            if tank.isWheeledVehicle:
                should_pop_elements = False
                randomize_chassis = False

            if not self.conf.fullTankRandomizer:
                # randomize each tank component (chassis, hull, gun) separately
                if randomize_chassis:
                    for i in range(chassis_count):
                        if self.conf.randomizeChassisSeparately:
                            index = random.randrange(0, len(self.tankChassisList))
                            random_chassis_list.append(self.tankChassisList[index])
                            if should_pop_elements:
                                self.tankChassisList.pop(index)
                        else:
                            random_chassis_list.append(hull_chassis)

                if self.conf.randomizeTurrets:
                    for i in range(turret_count):
                        index = random.randrange(0, len(self.tankTurretList))
                        random_turret_list.append(self.tankTurretList[index])
                        if should_pop_elements:
                            self.tankTurretList.pop(index)

                if self.conf.randomizeGuns:
                    for i in range(gun_count):
                        index = random.randrange(0, len(self.tankGunList))
                        random_gun_list.append(self.tankGunList[index])
                        if should_pop_elements:
                            self.tankGunList.pop(index)
            else:
                # find a random tank and use that tank's components
                random_tank = self.tankRootXmlList[random_hull_index]
                available_chassis = random_tank.find("chassis").findall("*")
                available_turrets = random_tank.find("turrets0").findall("*")
                available_guns = []
                for turret in available_turrets:
                    for gun in turret.find("guns").findall("*"):
                        available_guns.append(gun)

                for i in range(chassis_count):
                    index = random.randrange(0, len(available_chassis))
                    random_chassis_list.append(available_chassis[index])

                for i in range(turret_count):
                    index = random.randrange(0, len(available_turrets))
                    random_turret_list.append(available_turrets[index])

                for i in range(gun_count):
                    index = random.randrange(0, len(available_guns))
                    random_gun_list.append(available_guns[index])

            if should_pop_elements:
                self.tankHullList.pop(random_hull_index)
                self.tankRootXmlList.pop(random_hull_index)

            if self.conf.randomizeHulls:
                _remove_and_replace("AODecals", random_hull, tank.hull)
                xml.replace_element(random_hull.find("models"), tank.hull)
                xml.replace_element(random_hull.find("swinging"), tank.hull)
                xml.replace_element(random_hull.find("exhaust"), tank.hull)
                xml.replace_element(random_hull.find("turretPositions"), tank.hull)
                if xml.elementExists("turretPitches", random_hull):
                    xml.add_element(random_hull.find("turretPitches"), tank.hull)

                tank_hard_points = tank.hull.find("turretHardPoints")

                if tank_hard_points is not None:
                    xml.removeAllElementsByName("turretHardPoints", tank.hull)

                xml.replace_element(random_hull.find("turretHardPoints"), tank.hull)
                xml.removeAllElementsByName("variants", tank.hull)

            if randomize_chassis:
                for i in range(chassis_count):
                    chassis = tank.chassisList[i]
                    random_chassis = random_chassis_list[i]
                    # xml.replace_element(random_chassis.find("models"), chassis)
                    # xml.replace_element(random_chassis.find("AODecals"), chassis)
                    # xml.replace_element(random_chassis.find("wwsoundPC"), chassis)
                    # xml.replace_element(random_chassis.find("wwsoundNPC"), chassis)
                    # xml.replace_element(random_chassis.find("drivingWheels"), chassis)
                    # xml.replace_element(random_chassis.find("trackNodes"), chassis)
                    # xml.replace_element(random_chassis.find("groundNodes"), chassis)
                    # xml.replace_element(random_chassis.find("splineDesc"), chassis)
                    # xml.replace_element(random_chassis.find("wheels"), chassis)
                    # xml.replace_element(random_chassis.find("trackThickness"), chassis)
                    # xml.replace_element(random_chassis.find("tracks"), chassis)
                    # xml.replace_element(random_chassis.find("traces"), chassis)
                    # xml.replace_element(random_chassis.find("effects"), chassis)
                    # xml.replace_element(random_chassis.find("physicalTracks"), chassis)
                    # xml.removeAllElementsByName("leveredSuspension", chassis)
                    # xml.replace_element(random_chassis.find("leveredSuspension"), chassis)

                    # have to use this method which removes the element in the chassis section first
                    # otherwise the game would crash
                    _remove_and_replace("models", random_chassis, chassis)
                    _remove_and_replace("AODecals", random_chassis, chassis)
                    _remove_and_replace("wwsoundPC", random_chassis, chassis)
                    _remove_and_replace("wwsoundNPC", random_chassis, chassis)
                    _remove_and_replace("drivingWheels", random_chassis, chassis)
                    _remove_and_replace("trackNodes", random_chassis, chassis)
                    _remove_and_replace("groundNodes", random_chassis, chassis)
                    _remove_and_replace("splineDesc", random_chassis, chassis)
                    _remove_and_replace("wheels", random_chassis, chassis)
                    _remove_and_replace("trackThickness", random_chassis, chassis)
                    _remove_and_replace("tracks", random_chassis, chassis)
                    _remove_and_replace("traces", random_chassis, chassis)
                    _remove_and_replace("effects", random_chassis, chassis)
                    _remove_and_replace("physicalTracks", random_chassis, chassis)
                    _remove_and_replace("leveredSuspension", random_chassis, chassis)
                    _remove_and_replace("topRightCarryingPoint", random_chassis, chassis)

            if self.conf.randomizeTurrets:
                for i in range(turret_count):
                    turret = tank.turretList[i]
                    random_turret = random_turret_list[i]
                    # xml.replace_element(random_turret.find("models"), turret)
                    _remove_and_replace("models", random_turret, turret)
                    _remove_and_replace("ceilless", random_turret, turret)
                    _remove_and_replace("wwturretRotatorSoundManual", random_turret, turret)

                    # self.copy_customization(random_turret, turret)

            if self.conf.randomizeGuns:
                for i in range(gun_count):
                    gun = tank.gunList[i]
                    random_gun = random_gun_list[i]
                    xml.replace_element(random_gun.find("models"), gun)
                    xml.removeAllElementsByName("drivenJoints", gun)
                    xml.replace_element(random_gun.find("drivenJoints"), gun)

                    # self.copy_customization(random_gun, gun)

                    is_dual_gun = configLoader.parse_bool(xml.IsDoubleGunTag, random_gun, False)

                    # gun effects randomization
                    if self.conf.randomizeGunEffects:
                        comp = self.guns.getGun(random_gun.tag)
                        if self.conf.fullTankRandomizer and comp is not None:
                            # variable 'comp' is the gun from components/guns.xml
                            # variable 'gun' is one of the guns of the tank being currently randomized
                            xml.replace_element(comp.find("effects"), gun)
                            xml.replace_element(comp.find("reloadEffect"), gun)
                            xml.replace_element(comp.find("recoil"), gun)
                            xml.replace_element(comp.find("impulse"), gun)
                        else:
                            if not is_dual_gun:
                                effect_random_element = ET.Element("effects")
                                effect_random_element.text = self.conf.gunEffects[random.randrange(0, len(self.conf.gunEffects))]
                            else:
                                effect_random_element = ET.Element("multiGunEffects")
                                effect_l = self.conf.gunEffectsDual[random.randrange(0, len(self.conf.gunEffectsDual))]
                                effect_r = self.conf.gunEffectsDual[random.randrange(0, len(self.conf.gunEffectsDual))]
                                effect_random_element.text = effect_l + " " + effect_r

                            xml.add_element(effect_random_element, gun)

                            if comp is not None:
                                xml.replace_element(comp.find("reloadEffect"), gun)
                                xml.replace_element(comp.find("recoil"), gun)
                                xml.replace_element(comp.find("impulse"), gun)

            tank.tree.write(tank.path.replace("Source/", "Output/").replace("Addons/", "Output/"))