# simple-rest-test-client
Microframework for test rest api

## USAGE

### generic data for request

```
data = [{
    "json": {
        "arg": "foo"
    },
    "expect": {
    
        """
        Basic HTTP asserts
        """
    
        "status_code": 200, # default value
        "mime_type": "application/json" # default value
        
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
... 
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