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
    "vo_eb_overtime_defenders"]

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

    "imp_medium_critical_HE_",
    "imp_medium_not_pierce_HE_",
    "imp_medium_pierce_HE_",

    "imp_small_critical_HE_",
    "imp_small_not_pierce_HE_",
    "imp_small_pierce_HE_"
]


shellImpactSoundEventsListCopy = []

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

def loadBank(bank, doCopy):
    xml.insertElementEmptyNew("bank", bnks).text = bank
    if doCopy == True:
        copyfile('Source/res/audioww/' + bank, 'Output/res/audioww/'+bank)

def addEvent(name, mod, add):
    rand = xml.getRandomListIndex(mod, random)
    baseElement = xml.insertElementEmptyNew("event", events)
    xml.insertElement("name", name[i] + add, baseElement)

    if int(seed) == 666:
        xml.insertElement("mod", "imp_huge_pierce_HE_" + add, baseElement)
    else:
        xml.insertElement("mod", mod[rand] + add, baseElement)

    mod.pop(rand)

if randCustom == "true":

    if useAGS:

        loadBank("kk91_altGunSounds.bnk", True)

    if useOGS:

        loadBank("kk91_wpn_old.bnk", True)


if randVoice == "true":

    loadBank("epic_battle_voiceover.bnk", False)

    crewVoiceEventsListCopy = deepcopy(crewVoiceEventsList)

    for i in range(0, len(crewVoiceEventsList)):
        addEvent(crewVoiceEventsList, crewVoiceEventsListCopy, '')

if randImp == "true":

    shellImpactSoundEventsListCopy = deepcopy(shellImpactSoundEventsList)

    for i in range(0, len(crewVoiceEventsList)):
        addEvent(shellImpactSoundEventsList, shellImpactSoundEventsListCopy, 'NPC_NPC')

    shellImpactSoundEventsListCopy = deepcopy(shellImpactSoundEventsList)

    for i in range(0, len(crewVoiceEventsList)):
        addEvent(shellImpactSoundEventsList, shellImpactSoundEventsListCopy, 'PC_NPC')

    shellImpactSoundEventsListCopy = deepcopy(shellImpactSoundEventsList)

    for i in range(0, len(crewVoiceEventsList)):
        addEvent(shellImpactSoundEventsList, shellImpactSoundEventsListCopy, 'NPC_PC')

if randCustom == "true":
    loadBank("randomizer.bnk", True)

newtree = ET.ElementTree(root)
newtree.write(xmlpath)