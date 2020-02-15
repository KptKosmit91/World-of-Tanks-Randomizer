REQUIREMENTS:

-Python 3.7+ is required to run this tool. Older versions might work but it was only tested on this version.
You can download it here if you don't have it: https://www.python.org/downloads/release/python-375/
Remember to check "Add Python 3.7 to PATH" while installing it!
________________________________________________________________________________________________________________________________________

CURRENT FEATURES:

-Tank model randomizer
-Gun sound randomizer
-Shell impact sound randomizer
-Crew voice prompts randomizer
-Map music randomizer
-Map foliage randomizer
By default all the options are enabled. You can disable them in the config file.
________________________________________________________________________________________________________________________________________

USAGE:

Run generate.bat
Before running it you can also set your mod seed in Config/RandomizerConfig.xml. by default it is a random seed (setting it to 0 in the config will generate a random seed on every run)
Each seed provides different results in game!
Keep in mind, that changing the config won't alter existing .wotmod mods previously made by the program! You'll have to generate them again.
WARNING: Don't open folders beyond Output/res when running the randomizer, otherwise it will crash!
________________________________________________________________________________________________________________________________________

INSTALLING THE GENERATED MODS

After running the bat file and after the window displays "You are ready to install your mod!" go to the Output folder. Ignore the "res" folder. Copy the generated .wotmod file into World_of_Tanks/mods/(VersionFolder)
Don't confuse the "mods" folder with the "res_mods" folder!
And remember to only have one randomized mod installed in the game at a time.
________________________________________________________________________________________________________________________________________

Special Thanks to:

StranikS-Scan's Decompiled WoT for easy access to non-binary xml files ( github: https://github.com/StranikS-Scan/WorldOfTanks-Decompiled )
