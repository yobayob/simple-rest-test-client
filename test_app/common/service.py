# -*- coding: utf-8 -*-
import sys
import time
import unittest

from fabric.api import lcd, local

from simple_rest_test_client.config import settings
from simple_rest_test_client.generic import Client


class TestEvents(unittest.TextTestResult):
    def startTestRun(self):
        Service().start()

    def stopTestRun(self):
        Service().stop()


class Service(object):
    """
    managment cls for application
    """

    def init(self, branch):
        """
        init & deploy project
        """
        local('rm -rf %s' % settings.PROJECT_DIR)
        local('mkdir -p %s' % settings.PROJECT_DIR)
        with lcd(settings.PROJECT_DIR):
            local('git clone %s .' % settings.GIT)
            local('git fetch')
            local('git checkout %s' % branch)
            local('virtualenv -p python3.5 .venv')
            local('.venv/bin/pip3.5 install -r requirements.txt')
        return self

    def clear(self):
        """
        clear data for testing
        """
        Client('DELETE', '/mock/reset/')
        return self

    def start(self):
        with lcd(settings.PROJECT_DIR):
            if '--no-screen' not in sys.argv:
                local('screen -dmS mock .venv/bin/python3.5 manage.py run')
                for i in range(2):
                    try:
                        r = Client('GET', '/api/ping/')
                    except:
                        pass
                    else:
                        if r.status_code == 200:
                            break
                    time.sleep(1)
            else:
                local('.venv/bin/python3.5 manage.py run')
        return self

    def stop(self):
        local('screen -S mock -X quit')
        return self