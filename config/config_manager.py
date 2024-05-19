
import configparser
import os

# Gestion de la configuration à partir du fichier .ini en utilisant la Class ConfigManager
class ConfigManager:
    def __init__(self):
        self.config_parser = configparser.ConfigParser()
        config_file_path = os.path.abspath(os.path.join('config', 'config.ini'))
        self.config_parser.read(config_file_path)

    def __getitem__(self, section):
        return self.SectionProxy(self.config_parser[section])

    class SectionProxy:
        def __init__(self, section):
            self.section = section

        def __getitem__(self, option):
            return self.section[option]
        
        