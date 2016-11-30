from simple_rest_test_client.core.generic import BaseTestCase
from simple_rest_test_client.core.requests_api import Client


class TestStatusCode(BaseTestCase):
    method = 'POST'
    url = '/api/status_code/'

    request = [{
        'json':{'arg': 'foo'}
    },{
        'json': {'arg': 404},
        'expect':{
            'status_code': 404,
            'content_type': 'text/plain'
        }
    }]

    def client(self, arg=None, **kwargs):
        json = dict()
        if arg is not None:
            json['arg'] = arg
        return Client(self.method, self.url, json=json, **kwargs)


class TestSchema(BaseTestCase):
    method = 'POST'
    url = '/api/schema/'

    def client(self, arg=None, **kwargs):
        json = dict()
        if arg is not None:
            json['arg'] = arg
        return Client(self.method, self.url, json=json, **kwargs)