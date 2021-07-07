from configLoader import Config
from zipfile import ZipFile
import os


class WotmodMaker:
    conf: Config = None
    seed = 0

    def __init__(self, config: Config, seed):
        self.conf = config
        self.seed = seed

    def create_wotmod(self):
        name = self.conf.wotmodName.replace("$randver", self.conf.randomizerversion)\
            .replace("$wotver", self.conf.wotversion).replace("$seed", str(self.seed))

        wotmod = ZipFile('Output/' + name + '.wotmod', 'w')

        for folderName, subfolders, filenames in os.walk(self.conf.resPathOut):
            for filename in filenames:
                # create complete filepath of file in directory
                filePath = os.path.join(folderName, filename)
                # Add file to zip
                wotmod.write(filePath, arcname=filePath.replace("Output/", ""), compress_type=None, compresslevel=None)

        print("Packed wotmod file " + name + ".wotmod")
