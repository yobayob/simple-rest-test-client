from urlparse import urljoin

import requests
from jsonschema import Draft4Validator, validate, ValidationError
from validator import validate as validate_response

from simple_rest_test_client.config import settings


class ValidateResponse(object):

    def __init__(self, response, **kwargs):
        self.fails = list()
        self.response = response
        for k,v in kwargs.iteritems():
            setattr(self, k, v)
            if hasattr(self, 'assert_%s' % k):
                getattr(self, 'assert_%s' % k)()

    def _value(self):
        try:
            return self.response.json()
        except ValueError:
            return self.response.text

    def assert_error_codes(self):
        resp_error_codes = [item['code'] for item in self.response.json()['errors']]
        if len(resp_error_codes) == len(self.error_codes) \
                or set(resp_error_codes) == set(self.error_codes):
            self.fails.append("Incorrect list of errors %s") % self.response.json()['errors']

    def assert_status_code(self):
        if not self.response.status_code == self.status_code:
            self.fails.append('Status code is %d\nExpected code - %d' % (self.response.status_code,self.status_code))

    def assert_mime_type(self):
        if self.mime_type not in self.response.headers.get('content-type'):
            self.fails.append('Mime type is %s\n'
                              'Expected type - %s' % (self.response.headers.get('content-type'),
                                                      self.mime_type))

    def assert_schema(self):
        try:
            validate(self._value(), self.schema)
        except ValidationError, e:
            self.fails.append(str(e))

    def assert_schema_collection(self):
        for item in self._value():
            if not Draft4Validator(self.schema).is_valid(item) is True:
                try:
                    validate(item, self.schema_collection)
                except ValidationError, e:
                    self.fails.append(str(e))

    def assert_time(self):
        if self.time < self.response.elapsed.total_seconds():
            self.fails.append('Time to response is %f' % self.response.elapsed.total_seconds())

    def assert_answer(self):
        v = validate_response(self.answer, self._value())
        if v.valid == False:
            for k, v in v.errors.items():
                self.fails.append('%s: %s' % (k, v))

    def assert_answer_collection(self):
        for item in self._value()['data']:
            v = validate_response(self.answer_collection, item)
            if v.valid == False:
                for k, v in v.errors.items():
                    self.fails.append('%s: %s' % (k, v))


class Client(object):
    method = 'GET'
    url = settings.BASE_URL

    def __init__(self, method='GET', url='/', auth_params=None, **kwargs):
        self.checks = {
            'status_code': 200,
            'mime_type': 'application/json'
        }
        self.method = method
        self.url = urljoin(settings.BASE_URL, url)
        if auth_params is None:
            params = {
                "service": settings.AUTH_SERVICE,
                "token": settings.AUTH_TOKEN
            }
        else:
            params = auth_params
        if kwargs.get("params"):
            kwargs["params"].update(params)
        else:
            kwargs["params"] = params
        self.kwargs = kwargs
        self.response = self.send()

    def expect(self, **kwargs):
        self.checks.update(kwargs)
        v = ValidateResponse(self.response, **self.checks)
        assert not v.fails, \
            '\n%s - %s\nBody:\n%s\nErrors:\n%s\n%s' \
            % (self.response.request.method,
               self.response.request.url,
               self.response.request.body,
               '\n'.join(v.fails), self.response.text)
        return self

    def send(self):
        return getattr(requests, self.method.lower())(self.url, **self.kwargs)

    def __getattr__(self, item):
        return getattr(self.response, item, None)