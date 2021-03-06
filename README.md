# simple-rest-test-client

Microframework for test rest api
Wrapper on python unittest for test api. Basic asserts func for response and automatic generation test func (DDT).

## Example usage

### Generic data for request

```python

import validator

data = [{
    "json": {
        "arg": "foo"
    },
    "expect": {
    
        """
        Basic HTTP asserts
        """
    
        "status_code": 200, # default value, not necessary define
        "mime_type": "application/json" # default value, not necessary define
        
        """
        Check schema & answer
        """
        
        "answer": {  # see also http://validatorpy.readthedocs.io/en/latest/
            "ans": [Required, Equals("bar")
        },
        
        "schema":{ # see also https://pypi.python.org/pypi/jsonschema
            "type": "object",
            "required": ["ans"],
            "properties": {
                "ans": {
                    "type": "string",
                }
            }
        }
    }
},
... # + other test fixture
]
```

### create test class

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

see test_app for example

## Usage with pytest

create conftest.py 
~~~
import os
os.environ.setdefault("SRTC_CONF", "settings")
~~~

create settings.py
~~~
BASE_URL = 'http://127.0.0.1:5000'

AUTH_TYPE = 'token-service'
AUTH_TOKEN = 'test'
AUTH_SERVICE = 'test'
~~~