# simple-rest-test-client
Microframework for test rest api

# USAGE

```python

from simple_rest_test_client.core.generic import BaseTestCase
from simple_rest_test_client.core.requests_api import Client

class TestStatusCode(BaseTestCase):
    method = 'POST'
    url = '/api/status_code/'
    requests = data

    def client(self, arg=None, **kwargs):
        """
        make custom client
        """
        json = dict()
        if arg is not None:
            json['arg'] = arg
        return Client(self.method, self.url, json=json, **kwargs)

```