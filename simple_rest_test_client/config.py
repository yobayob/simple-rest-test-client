import os
from importlib import *

import global_settings

ENVIRONMENT_VARIABLE = 'SRTC_CONF'


class Settings(object):

    def __init__(self):
        for setting in dir(global_settings):
            if setting.isupper():
                setattr(self, setting, getattr(global_settings, setting))


class LazySettings(object):

    def __init__(self):
        self.settings = Settings()
        self.settings_module = os.environ.get(ENVIRONMENT_VARIABLE)

    def make_settings(self):

        conf = import_module(self.settings_module)

        for setting in dir(conf):
            if setting.isupper():
                setting_value = getattr(conf, setting)
                setattr(self.settings, setting, setting_value)
        return self.settings

settings = LazySettings().make_settings()