import os
from importlib import *
import global_settings


ENVIRONMENT_VARIABLE = 'SRTC_CONF'


class LazySettings(object):

    def __init__(self):
        self.settings = set()
        self.settings_module = os.environ.get(ENVIRONMENT_VARIABLE)

    def make_settings(self):
        for setting in dir(global_settings):
            if setting.isupper():
                setattr(self, setting, getattr(global_settings, setting))
        conf = import_module(self.settings_module)

        for setting in dir(conf):
            if setting.isupper():
                setting_value = getattr(conf, setting)
                setattr(self, setting, setting_value)
        return self

settings = LazySettings().make_settings().settings