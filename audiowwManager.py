from typing import List, Any

from copy import deepcopy

from configLoader import Config
import xml.etree.ElementTree as ET
import os

import xmlMethods as xml

from time import sleep
from shutil import copyfile
import random


class AudiowwManager:

    crewVoiceEventsList = [
        "vo_ally_killed_by_player",
        "vo_ammo_bay_damaged",
        "vo_armor_not_pierced_by_player",
        "vo_armor_ricochet_by_player",
        "vo_commander_killed",
        "vo_crew_deactivated",
        "vo_damage_by_near_explosion_by_enemy",
        "vo_damage_by_near_explosion_by_player",
        "vo_driver_killed",
        "vo_enemy_fire_started_by_player",
        "vo_enemy_hp_damaged_by_explosion_at_direct_hit_by_player",
        "vo_enemy_hp_damaged_by_projectile_and_chassis_damaged_by_player",
        "vo_enemy_hp_damaged_by_projectile_and_gun_damaged_by_player",
        "vo_enemy_hp_damaged_by_projectile_by_player",
        "vo_enemy_killed",
        "vo_enemy_killed_by_player",
        "vo_enemy_no_hp_damage_at_attempt_and_chassis_damaged_by_player",
        "vo_enemy_no_hp_damage_at_attempt_and_gun_damaged_by_player",
        "vo_enemy_no_hp_damage_at_no_attempt_and_chassis_damaged_by_player",
        "vo_enemy_no_hp_damage_at_no_attempt_and_gun_damaged_by_player",
        "vo_enemy_no_hp_damage_at_no_attempt_by_player",
        "vo_engine_damaged",
        "vo_engine_destroyed",
        "vo_engine_functional",
        "vo_fire_started",
        "vo_fire_stopped",
        "vo_fuel_tank_damaged",
        "vo_gun_damaged",
        "vo_gun_destroyed",
        "vo_gun_functional",
        "vo_gunner_killed",
        "vo_loader_killed",
        "vo_radio_damaged",
        "vo_radioman_killed",
        "vo_start_battle",
        "vo_surveying_devices_crit_damaged",
        "vo_surveying_devices_damaged",
        "vo_surveying_devices_destroyed",
        "vo_surveying_devices_functional",
        "vo_target_captured",
        "vo_target_lost",
        "vo_target_unlocked",
        "vo_track_damaged",
        "vo_track_destroyed",
        "vo_track_functional",
        "vo_track_functional_can_move",
        "vo_turret_rotator_damaged",
        "vo_turret_rotator_destroyed",
        "vo_turret_rotator_functional",
        "vo_vehicle_destroyed",
        "vo_dp_assistance_been_requested",
        "vo_dp_been_excluded_platoon",
        "vo_dp_left_platoon",
        "vo_dp_platoon_created",
        "vo_dp_platoon_dismissed",
        "vo_dp_platoon_joined",
        "vo_dp_player_joined_platoon",
        "vo_flt_ready_for_action",
        "vo_flt_repair",
        "vo_eb_promotion_received",
        "vo_eb_retreat_successful",
        "vo_eb_support_inspire",


        "vo_eb_zone_captured_ally_other_A",
        "vo_eb_zone_captured_ally_other_B",
        "vo_eb_zone_captured_ally_other_C",
        "vo_eb_zone_captured_ally_other_D",
        "vo_eb_zone_captured_ally_other_E",
        "vo_eb_zone_captured_ally_other_F",
        "vo_eb_zone_captured_ally_own_A",
        "vo_eb_zone_captured_ally_own_B",
        "vo_eb_zone_captured_ally_own_C",
        "vo_eb_zone_captured_ally_own_D",
        "vo_eb_zone_captured_ally_own_E",
        "vo_eb_zone_captured_ally_own_F",
        "vo_eb_zone_contested_defenders_A",
        "vo_eb_zone_contested_defenders_B",
        "vo_eb_zone_contested_defenders_C",
        "vo_eb_zone_contested_defenders_D",
        "vo_eb_zone_contested_defenders_E",
        "vo_eb_zone_contested_defenders_F",

        "vo_eb_objective_under_attack_attackers_3",


        "vo_eb_zone_contested_attackers_A",
        "vo_eb_zone_contested_attackers_B",
        "vo_eb_zone_contested_attackers_C",
        "vo_eb_zone_contested_attackers_D",
        "vo_eb_zone_contested_attackers_E",
        "vo_eb_zone_contested_attackers_F",
        "vo_eb_zone_lost_defender_other_A",
        "vo_eb_zone_lost_defender_other_B",
        "vo_eb_zone_lost_defender_other_C",
        "vo_eb_zone_lost_defender_other_D",
        "vo_eb_zone_lost_defender_other_E",
        "vo_eb_zone_lost_defender_other_F",
        "vo_eb_zone_lost_defender_own_A",
        "vo_eb_zone_lost_defender_own_B",
        "vo_eb_zone_lost_defender_own_C",
        "vo_eb_zone_lost_defender_own_D",
        "vo_eb_zone_lost_defender_own_E",
        "vo_eb_zone_lost_defender_own_F",
        "vo_eb_support_artillery",
        "vo_eb_support_smoke_screen",
        "vo_eb_overtime_attackers",
        "vo_eb_overtime_defenders"
        "vo_eb_all_destroyed_attackers",
        "vo_eb_all_lost_defenders",
        "vo_eb_allied_general_enters",
        "vo_eb_allies_destroyed",
        "vo_eb_ally_reinforcement_arrived",
        "vo_eb_deployment_ready",
        "vo_eb_last_objective_attackers",
        "vo_eb_last_objective_defenders",
        "vo_eb_last_zone_attackers",
        "vo_eb_last_zone_attackers_other",
        "vo_eb_last_zone_defenders",
        "vo_eb_last_zone_defenders_other",
        "vo_eb_no_time_attackers",
        "vo_eb_no_time_defenders",
        "vo_eb_start_defenders",
        "vo_eb_start_attackers"
    ]

    shellImpactSoundEventsList = [
        "imp_auto_critical_AP_",
        "imp_auto_not_pierce_AP_",
        "imp_auto_pierce_AP_",
        "imp_auto_ricochet_AP_",

        "imp_auto_critical_APCR_",
        "imp_auto_not_pierce_APCR_",
        "imp_auto_pierce_APCR_",
        "imp_auto_ricochet_APCR_",

        "imp_huge_critical_AP_",
        "imp_huge_not_pierce_AP_",
        "imp_huge_pierce_AP_",
        "imp_huge_ricochet_AP_",

        "imp_large_critical_AP_",
        "imp_large_not_pierce_AP_",
        "imp_large_pierce_AP_",
        "imp_large_ricochet_AP_",

        "imp_main_critical_AP_",
        "imp_main_not_pierce_AP_",
        "imp_main_pierce_AP_",
        "imp_main_ricochet_AP_",

        "imp_medium_critical_AP_",
        "imp_medium_not_pierce_AP_",
        "imp_medium_pierce_AP_",
        "imp_medium_ricochet_AP_",

        "imp_small_critical_AP_",
        "imp_small_not_pierce_AP_",
        "imp_small_pierce_AP_",
        "imp_small_ricochet_AP_",

        "imp_huge_critical_APCR_",
        "imp_huge_not_pierce_APCR_",
        "imp_huge_pierce_APCR_",
        "imp_huge_ricochet_APCR_",

        "imp_large_critical_APCR_",
        "imp_large_not_pierce_APCR_",
        "imp_large_pierce_APCR_",
        "imp_large_ricochet_APCR_",

        "imp_main_critical_APCR_",
        "imp_main_not_pierce_APCR_",
        "imp_main_pierce_APCR_",
        "imp_main_ricochet_APCR_",

        "imp_medium_critical_APCR_",
        "imp_medium_not_pierce_APCR_",
        "imp_medium_pierce_APCR_",
        "imp_medium_ricochet_APCR_",

        "imp_small_critical_APCR_",
        "imp_small_not_pierce_APCR_",
        "imp_small_pierce_APCR_",
        "imp_small_ricochet_APCR_",

        "imp_huge_critical_HC_",
        "imp_huge_not_pierce_HC_",
        "imp_huge_pierce_HC_",
        "imp_huge_ricochet_HC_",

        "imp_large_critical_HC_",
        "imp_large_not_pierce_HC_",
        "imp_large_pierce_HC_",
        "imp_large_ricochet_HC_",

        "imp_main_critical_HC_",
        "imp_main_not_pierce_HC_",
        "imp_main_pierce_HC_",
        "imp_main_ricochet_HC_",

        "imp_medium_critical_HC_",
        "imp_medium_not_pierce_HC_",
        "imp_medium_pierce_HC_",
        "imp_medium_ricochet_HC_",

        "imp_small_critical_HC_",
        "imp_small_not_pierce_HC_",
        "imp_small_pierce_HC_",
        "imp_small_ricochet_HC_",

        "imp_huge_critical_HE_",
        "imp_huge_not_pierce_HE_",
        "imp_huge_pierce_HE_",

        "imp_large_critical_HE_",
        "imp_large_not_pierce_HE_",
        "imp_large_pierce_HE_",

        "imp_main_critical_HE_",
        "imp_main_not_pierce_HE_",
        "imp_main_pierce_HE_",

        "imp_medium_critical_HE_",
        "imp_medium_not_pierce_HE_",
        "imp_medium_pierce_HE_",

        "imp_small_critical_HE_",
        "imp_small_not_pierce_HE_",
        "imp_small_pierce_HE_",

        "imp_artillery_expl_huge_",
        "imp_artillery_expl_large_",
        "imp_artillery_expl_main_"
    ]

    shellGroundImpactSoundEventsList = [
        "imp_surface_automatic_",
        "imp_surface_huge_",
        "imp_surface_large_",
        "imp_surface_main_",
        "imp_surface_medium_",
        "imp_surface_small_"
    ]

    artySurfaceImpact = [
        "imp_artillery_expl_surface_huge",
        "imp_artillery_expl_surface_large",
        "imp_artillery_expl_surface_main",
    ]

    shellHESplashImpactSoundEventsList = [
        "imp_huge_splash_HE_NPC_PC",
        "imp_large_splash_HE_NPC_PC",
        "imp_main_splash_HE_NPC_PC",
        "imp_medium_splash_HE_NPC_PC",
        "imp_small_splash_HE_NPC_PC",
        "imp_artillery_splash_huge_NPC_PC",
        "imp_artillery_splash_large_NPC_PC",
        "imp_artillery_splash_main_NPC_PC",
    ]

    conf: Config = None

    bankFilePaths: list[str] = []
    bankFileNames: list[str] = ["epic_battle_voiceover.bnk"]

    events_section: ET.Element

    def __init__(self, config: Config, seed: int):
        random.seed(seed)
        self.conf = config

    def gather_information(self):

        folder = self.conf.audiowwPath
        if os.path.exists(folder):
            for file_name in os.listdir(folder):
                if file_name.lower().endswith(".bnk") or file_name.lower().endswith(".pck"):
                    self.bankFilePaths.append(folder + file_name)
                    self.bankFileNames.append(file_name)

        for addon in self.conf.activeAddons:
            folder = self.conf.audiowwPath.replace("Source/", addon)
            if os.path.exists(folder):
                for file_name in os.listdir(folder):
                    if file_name.lower().endswith(".bnk") or file_name.lower().endswith(".pck"):
                        self.bankFilePaths.append(folder + file_name)
                        self.bankFileNames.append(file_name)

    def create_audiomodsxml(self):
        path = "Source/audio_mods_template.xml"
        tree = ET.parse(path)
        root = tree.getroot()

        load_banks_section = root.find("loadBanks")

        for bank in self.bankFileNames:
            element = ET.Element("bank")

            name = ET.Element("name")
            name.text = bank

            priority = ET.Element("priority")
            priority.text = "50"

            element.append(name)
            element.append(priority)

            load_banks_section.append(element)

        for i in range(0, len(self.bankFilePaths)):
            copyfile(self.bankFilePaths[i], self.conf.audiowwPathOut + self.bankFileNames[i])

        self.events_section = root.find("events")

        if self.events_section is not None:
            self.randomize(self.events_section)
        else:
            print("Failed to randomize sounds! Source/audio_mods_template.xml structure might be wrong.")
            sleep(5)

        tree.write(self.conf.audiowwPathOut + "audio_mods.xml")

    def randomize(self, events_section):

        print("\nRandomizing Sounds\n")

        print("Randomizing crew voices")
        self.randomize_from_list(self.crewVoiceEventsList, '', 'crew')

        print("Randomizing shell impact sounds")
        self.randomize_from_list(self.shellImpactSoundEventsList, 'NPC_NPC', 't_imp')
        self.randomize_from_list(self.shellImpactSoundEventsList, 'PC_NPC', 't_imp')
        self.randomize_from_list(self.shellImpactSoundEventsList, 'NPC_PC', 't_imp')
        self.randomize_from_list(self.shellHESplashImpactSoundEventsList, '', 't_imp')
        self.randomize_from_list(self.shellGroundImpactSoundEventsList, 'NPC', 'g_imp')
        self.randomize_from_list(self.shellGroundImpactSoundEventsList, 'PC', 'g_imp')
        self.randomize_from_list(self.artySurfaceImpact, '', 'g_imp')

        print("\nSound randomization done\n")

    def randomize_from_list(self, event_list, add, sound_type):
        copy_list = deepcopy(event_list)

        for i in range(0, len(event_list)):
            # self.randomize_sound_event(event_list, copy_list, add, sound_type, i)

            rand = xml.getRandomListIndex(copy_list, random)
            base_element = xml.insertElementEmptyNew("event", self.events_section)
            xml.insertElement("name", event_list[i] + add, base_element)
            xml.insertElement("mod", copy_list[rand] + add, base_element)
            copy_list.pop(rand)
