from simple_rest_test_client.core.generic import BaseTestCase
from simple_rest_test_client.core.requests_api import Client
from fixture import data, mock
from common.service import Service


class TestStatusCode(BaseTestCase):
    method = 'POST'
    url = '/api/status_code/'
    requests = data

    @classmethod
    def setUpClass(cls):
        Service().clear()
        response = Client("PUT", '/mock/add/', json=mock)
        response.expect()

    def client(self, arg=None, **kwargs):
        """
        make custom client
        """
        json = dict()
        if arg is not None:
            json['arg'] = arg
        return Client(self.method, self.url, json=json, **kwargs)