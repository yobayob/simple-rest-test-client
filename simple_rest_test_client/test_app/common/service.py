# -*- coding: utf-8 -*-
import sys
import unittest
from fabric.api import *
from simple_rest_test_client.core.generic import Client
import time


class TestEvents(unittest.TextTestResult):
    def startTestRun(self):
        pass

    def stopTestRun(self):
        pass


class Service(object):
    """
    managment cls for application
    """

    def init(self):
        """
        init & deploy project
        """
        # Create dir and clone project
        if os.path.isfile(cnf.GOPATH) is False:
            local('rm -rf ' + cnf.GOPATH)
            local('mkdir -p ' + cnf.PROJECT_DIR)
            with lcd(cnf.PROJECT_DIR):
                local('git clone ' + cnf.GIT + ' .')

        with lcd(cnf.PROJECT_DIR):
            local('git fetch')
            local('git checkout ' + branch)
        return self

    def clear(self):
        """
        clear data for testing
        """
        return self

    def start(self):
        with lcd(settings.PROJECT_DIR):
            if '--no-screen' not in sys.argv:
                local('screen -dmS ms_comment_test ./bin run')
                for i in range(15):
                    try:
                        r = Client('GET', '/api/ping/')
                    except:
                        pass
                    else:
                        if r.status_code == 200:
                            break
                    time.sleep(1)
            else:
                local('./bin run')
        return self

    def stop(self):
        local('screen -S ms_comment_test -X quit')
        return self