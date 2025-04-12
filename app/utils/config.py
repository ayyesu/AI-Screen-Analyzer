import os
import configparser

class ConfigManager:
    def __init__(self, config_file='config.ini'):
        self.config = configparser.ConfigParser()
        self.config_file = config_file
        self.load_config()

    def load_config(self):
        # Default config
        if not os.path.exists(self.config_file):
            self.config['API'] = {
                'gemini_api_key': '',
                'hotkey': 'ctrl+shift+s'
            }
            self.config['Settings'] = {
                'mode': 'auto',  # auto, code, general
                'code_formatting': 'True'
            }
            with open(self.config_file, 'w') as f:
                self.config.write(f)
        else:
            self.config.read(self.config_file)
            # Ensure all sections exist
            if 'Settings' not in self.config:
                self.config['Settings'] = {
                    'mode': 'auto',
                    'code_formatting': 'True'
                }
                self.save_config()

    def save_config(self):
        with open(self.config_file, 'w') as f:
            self.config.write(f)

    def get(self, section, key, fallback=None):
        return self.config.get(section, key, fallback=fallback)

    def getboolean(self, section, key, fallback=None):
        return self.config.getboolean(section, key, fallback=fallback)

    def set(self, section, key, value):
        if section not in self.config:
            self.config[section] = {}
        self.config[section][key] = str(value)
        self.save_config()
