import os

SERVER_HOST = 'localhost'
SERVER_PORT = 5000
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_URL = 'http://%s:%d/' % (SERVER_HOST, SERVER_PORT)

PROJECT_DIR = os.path.join('/tmp/test_server')
AUTH_TYPE = 'token-service'

AUTH_TOKEN = 'test'
AUTH_SERVICE = 'test'

GIT = 'https://github.com/yobayob/simple-mock-server'