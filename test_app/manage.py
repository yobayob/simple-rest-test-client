# -*- coding: utf-8 -*-

import sys
import unittest
import xmlrunner
import os

if __name__ == "__main__":

    os.environ.setdefault("SRTC_CONF", "settings")

    from common.service import Service, TestEvents

    if len(sys.argv) > 1 and sys.argv[1] == 'init':
        branch = 'master'
        if len(sys.argv) > 2:
            branch = sys.argv[2]
        Service().init(branch=branch)

    elif len(sys.argv) > 1 and sys.argv[1] in ['start', 'run', 'runserver']:
        Service().start()

    elif len(sys.argv) > 1 and sys.argv[1] == 'stop':
        Service().stop()

    elif len(sys.argv) > 1 and sys.argv[1] == 'restart':
        Service().stop().start()

    elif len(sys.argv) > 1 and sys.argv[1] in ['test', 'test-junit']:

        if len(sys.argv) >= 3:
            testsuite = unittest.TestLoader().loadTestsFromName('tests.'+sys.argv[2])
        else:
            testsuite = unittest.TestLoader().discover('.')
        if sys.argv[1] == 'test':
            unittest.TextTestRunner(resultclass=TestEvents).run(testsuite)
        else:
            xmlrunner.XMLTestRunner(output='test-reports', resultclass=TestEvents).run(testsuite)
    else:
        getattr(Service(), sys.argv[1])()