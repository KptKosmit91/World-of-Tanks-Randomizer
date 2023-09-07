import os
import xml.etree.ElementTree as ET


def _parse_error(var_type: str, name: str, in_section, default):
    if in_section is None:
        print(f"Failed to load {var_type} {name} from <null>! Defaulting to '{str(default)}'")
    else:
        print(f"Failed to load {var_type} {name} from section {in_section.tag}! Defaulting to '{str(default)}'")


def parse_string(name: str, in_section: ET.Element, default: str):
    if in_section is None:
        _parse_error("string", name, in_section, default)
        return default

    element = in_section.find(name)

    if element is None:
        _parse_error("string", name, in_section, default)
        return default

    text = element.text

    if text is None:
        return ""

    return text


def parse_bool(name: str, in_section: ET.Element, default: bool):
    if in_section is None:
        _parse_error("bool", name, in_section, default)
        return default

    element = in_section.find(name)

    if element is None:
        _parse_error("bool", name, in_section, default)
        return default

    text = element.text.lower()

    if text == "false" or text == "no" or text == "0":
        return False

    if text == "true" or text == "yes" or text == "1":
        return True

    return False


def parse_int(name: str, in_section: ET.Element, default: int):
    if in_section is None:
        _parse_error("integer", name, in_section, default)
        return default

    element = in_section.find(name)

    if element is None:
        _parse_error("integer", name, in_section, default)
        return default

    # text = element.text.lower()

    return int(element.text)


def string_hashcode(s):
    h = 0
    for c in s:
        h = (31 * h + ord(c)) & 0xFFFFFFFF
    return ((h + 0x80000000) & 0xFFFFFFFF) - 0x80000000


class ConfigLoader:

    configPath = "Config/RandomizerConfig.xml"

    @classmethod
    def load_config(cls):
        print("Loading randomizer config " + cls.configPath + "\n")

        tree = ET.parse(cls.configPath)
        root = tree.getroot()

        addon_section = root.find("Addons")

        addons = os.listdir(Config.addonsPath)
        for addon in addons:
            if os.path.isdir(Config.addonsPath + addon):
                is_addon_active = parse_bool("Use"+addon, addon_section, True)

                print(f"Found addon {addon}. Is active: {is_addon_active}")

                if is_addon_active:
                    Config.activeAddons.append(Config.addonsPath + addon.replace(" ", "_") + "/Source/")

        try:
            Config.seed = parse_int("Seed", root, 0)
        except ValueError:
            string = root.find("Seed").text

            # seed = 0
            #
            # for char in string:
            #     seed += ord(char)

            Config.seed = string_hashcode(string)

        tank_section = root.find("TankRandomizer")

        keywords = parse_string("Keywords", tank_section, "").replace(",", " ").split()

        Config.keywords = keywords

        if len(keywords) == 0:
            print("Keywords: None")
            Config.tankRandomizationIsUnique = parse_bool("UniqueRandomization", tank_section, True)
        else:
            print(f"Keywords: {keywords}")
            print("Keywords are present. UniqueRandomization won't be used and will be set to false")
            Config.tankRandomizationIsUnique = False

        Config.fullTankRandomizer = parse_bool("TankSwap", tank_section, False)
        Config.randomizeChassisSeparately = parse_bool("RandomizeChassisSeparately", tank_section, False)

        Config.randomizeHulls = parse_bool("RandomizeHulls", tank_section, True)
        Config.randomizeChassis = parse_bool("RandomizeChassis", tank_section, True)
        Config.randomizeTurrets = parse_bool("RandomizeTurrets", tank_section, True)
        Config.randomizeGuns = parse_bool("RandomizeGuns", tank_section, True)
        Config.randomizeGunEffects = parse_bool("RandomizeGunEffects", tank_section, True)


        Config.randomizeDamageStickers = parse_bool("RandomizeDamageDecals", tank_section, True)
        Config.randomizeVehicleEffects = parse_bool("RandomizeVehicleEffects", tank_section, True)
        Config.randomizeShotEffects = parse_bool("RandomizeShellEffects", tank_section, True)

        Config.randomizePaints = parse_bool("RandomizePaints", tank_section, True)
        Config.randomizeCamos = parse_bool("RandomizeCamos", tank_section, True)

        print("Config loaded!")


class Config:
    wotmodName = "Randomizer_v$randver_$wotver_Seed=$seed"
    randomizerversion = "1.0"
    wotversion = "1.22.0"

    resPath = "Source/res/"
    resPathOut = "Output/res/"

    audiowwPath = "Source/res/audioww/"
    audiowwPathOut = "Output/res/audioww/"

    mapsPath = "Source/res/scripts/arena_defs/"
    mapsPathOut = "Output/res/scripts/arena_defs/"

    itemDefsPath = "Source/res/scripts/item_defs/"
    itemDefsPathOut = "Output/res/scripts/item_defs/"

    tanksPath = "Source/res/scripts/item_defs/vehicles/"
    tanksPathOut = "Output/res/scripts/item_defs/vehicles/"

    shotEffectsPath = "Source/res/scripts/item_defs/vehicles/common/shot_effects.xml"
    shotEffectsPathOut = "Output/res/scripts/item_defs/vehicles/common/shot_effects.xml"

    vehEffectsPath = "Source/res/scripts/item_defs/vehicles/common/vehicle_effects.xml"
    vehEffectsPathOut = "Output/res/scripts/item_defs/vehicles/common/vehicle_effects.xml"

    dmgStickersPath = "Source/res/scripts/item_defs/vehicles/common/damage_stickers.xml"
    dmgStickersPathOut = "Output/res/scripts/item_defs/vehicles/common/damage_stickers.xml"

    customizationPath = "Source/res/scripts/item_defs/customization/"

    addonsPath = "Addons/"

    # addonNewTankModelsPath = "Addons/NewTankModels/"
    # addonNewTankModelsVehiclesPath = "Addons/NewTankModels/Source/res/scripts/item_defs/vehicles/"

    seed = 0

    keywords: str = ""

    tankRandomizationIsUnique = True
    fullTankRandomizer = True
    randomizeChassisSeparately = False

    randomizeHulls = True
    randomizeChassis = True
    randomizeTurrets = True
    randomizeGuns = True
    randomizeGunEffects = True

    randomizeDamageStickers = True
    randomizeVehicleEffects = True
    randomizeShotEffects = True

    randomizePaints = True
    randomizeCamos = True

    activeAddons = []

    countryFolders = {
        "Ch": "china",
        "Cz": "czech",
        "F": "france",
        "G": "germany",
        "It": "italy",
        "J": "japan",
        "Pl": "poland",
        "S": "sweden",
        "GB": "uk",
        "A": "usa",
        "R": "ussr"
    }

    vehicleModelsCountryFolders = {
        "Ch": "chinese",
        "Cz": "czech",
        "F": "french",
        "G": "german",
        "It": "italy",
        "J": "japan",
        "Pl": "poland",
        "S": "sweden",
        "GB": "british",
        "A": "american",
        "R": "russian"
    }

    gunEffects = []
    gunEffectsDual = []

    temp_BlackListedTanks = [
        "Env_Artillery",
        "Observer",
        
        "G79_Pz_IV_AusfGH",
        "A08_T23",
        "A15_T57",
        "A26_T18",
        "R05_KV",
        "R70_T_50_2",
        "G98_Waffentrager_E100_WO",

        "J27_O_I_120_BP",
        
        "R77_KV2_turret_2",
        "R95_Object_907A",
        "Cz17_Vz_55_CN",
        
        "R115_IS-3_auto_test",
        "R165_Object_703_II_2",
        "R165_Object_703_II_2_siege_mode",
        
        "R46_KV-13_SH",
        "R46_KV-13_SH_siege_mode",
        "F43_AMC_35_SH",
        "F43_AMC_35_SH_siege_mode",
        "A72_T25_2_SH",
        "GB107_Cavalier_SH",
        "G24_VK3002DB_SH",
        "Pl17_DS_PZlnz_SH",
        "S14_Ikv_103_SH",
        "S14_Ikv_103_SH_siege_mode",
        "Ch24_Type64_SH",

        "Ch00_ClingeBot_SH"
    ]

    @classmethod
    def is_tank_blacklisted(cls, tank: str):
        if not tank.lower().endswith(".xml"):
            return True
        if tank.lower() == "customization.xml":
            return True
        if tank.lower() == "list.xml":
            return True
        if tank.lower().endswith("_igr.xml"):
            return True
        if tank.lower().endswith("_bot.xml"):
            return True
        if tank.lower().endswith("_test.xml"):
            return True

        return tank.lower() in cls.temp_BlackListedTanks # the blacklist is converted to store all tanks in lowercase, so this works


for i in range(len(Config.temp_BlackListedTanks)):
    Config.temp_BlackListedTanks[i] = Config.temp_BlackListedTanks[i].lower() + ".xml"