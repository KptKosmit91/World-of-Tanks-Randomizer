import xml.etree.ElementTree as ET
import xmlMethods as xml
import config as conf
import os
import random
import fileMethods as fm
from shutil import copyfile
from copy import deepcopy

randVoice = conf.RandomizeCrewPrompts
randImp = conf.RandomizeShellImpactSounds
randCustom = conf.CustomSounds

useAGS = conf.UseAlternativeGunSoundsMod
useOGS = conf.UseOldGunSoundsMod

xmlpath = "Output/res/audioww/audio_mods.xml"

crewVoiceEventsList=[
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

crewVoiceEventsListCopy = []

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
    "imp_small_pierce_HE_"
]
shellImpactSoundEventsListCopy = []


shellGroundImpactSoundEventsList = [
    "imp_surface_automatic_",
    "imp_surface_huge_",
    "imp_surface_large_",
    "imp_surface_main_",
    "imp_surface_medium_",
    "imp_surface_small_"
]
shellGroundImpactSoundEventsListCopy = []


shellHESplashImpactSoundEventsList = [
    "imp_huge_splash_HE_NPC_PC",
    "imp_large_splash_HE_NPC_PC",
    "imp_main_splash_HE_NPC_PC",
    "imp_medium_splash_HE_NPC_PC",
    "imp_small_splash_HE_NPC_PC",
]
shellHESplashImpactSoundEventsListCopy = []

seed = conf.seed

random.seed(seed)

def createAudioXML():
    content = "<audio_mods.xml>\n<loadBanks>\n</loadBanks>\n<events>\n</events>\n</audio_mods.xml>"
    fm.createFolder("Output/res/audioww/")
    fm.createFile(xmlpath, content)

createAudioXML()

tree = ET.parse(xmlpath)
root = tree.getroot()
events = root.find("events")
bnks = root.find("loadBanks")

def addBankToLoad(bank, doCopy):
    xml.insertElementEmptyNew("bank", bnks).text = bank
    if doCopy == True:
        copyfile('Source/res/audioww/' + bank, 'Output/res/audioww/'+bank)

def randomizeSoundEvent(name, mod, add, soundtype, i):
    rand = xml.getRandomListIndex(mod, random)
    baseElement = xml.insertElementEmptyNew("event", events)
    xml.insertElement("name", name[i] + add, baseElement)
    xml.insertElement("mod", mod[rand] + add, baseElement)

    if soundtype == "t_imp":
        if int(seed) == 666:
            xml.insertElement("mod", "imp_huge_pierce_HE_" + add, baseElement)
    elif soundtype == "g_imp":
        if int(seed) == 666:
            xml.insertElement("mod", "imp_surface_huge_" + add, baseElement)

    mod.pop(rand)

def addSoundRandomization(list1, list1copy, add, soundtype):
    list1copy = deepcopy(list1)

    for i in range(0, len(list1)):
        randomizeSoundEvent(list1, list1copy, add, soundtype, i)

if randCustom == "true":

    if useAGS:

        addBankToLoad("kk91_altGunSounds.bnk", True)

    if useOGS:

        addBankToLoad("kk91_wpn_old.bnk", True)


if randVoice == "true":

    addBankToLoad("epic_battle_voiceover.bnk", False)

    addSoundRandomization(crewVoiceEventsList, crewVoiceEventsListCopy , '', 'crew')
    print("Crew prompts randomization completed successfully.")

if randImp == "true":

    addSoundRandomization(shellImpactSoundEventsList, shellImpactSoundEventsListCopy , 'NPC_NPC', 't_imp')
    addSoundRandomization(shellImpactSoundEventsList, shellImpactSoundEventsListCopy , 'PC_NPC', 't_imp')
    addSoundRandomization(shellImpactSoundEventsList, shellImpactSoundEventsListCopy , 'NPC_PC', 't_imp')
    addSoundRandomization(shellHESplashImpactSoundEventsList, shellHESplashImpactSoundEventsListCopy , '', 't_imp')
    addSoundRandomization(shellGroundImpactSoundEventsList, shellGroundImpactSoundEventsListCopy , 'NPC', 'g_imp')
    addSoundRandomization(shellGroundImpactSoundEventsList, shellGroundImpactSoundEventsListCopy , 'PC', 'g_imp')
    print("Impact sound randomization completed successfully.")

if randCustom == "true":
    addBankToLoad("randomizer.bnk", True)

newtree = ET.ElementTree(root)
newtree.write(xmlpath)