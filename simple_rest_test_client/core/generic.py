from unittest import TestCase
from config import settings
from requests_api import Client


class MetaTestMixin(type):

    @classmethod
    def create_a_function(cls,json=None, params=None,
                          expect=None, mock=None, setup=None, **kwargs):
        """
        :param setup: setup before test
        :param json: client args for request_api
        :param params: get-param
        :param expect: expected resuld for validate response
        :param mock: {} for one or [] for some // put mock obj to mock service
        :return: Response
        """
        def base_request(self, *args):
            if params is not None:
                params.update(params)
            if mock is not None:
                self.put_mock(mock)
            client_kwargs = self.get_client_kwargs()
            if json is not None:
                client_kwargs.update(json)
            response = self.client(params=params, **client_kwargs)
            if expect is not None:
                response.expect(**expect)
            else:
                response.expect()
            return response
        return base_request

    def __new__(mcs, name, base, dict):
        cls = super(MetaTestMixin, mcs).__new__(mcs, name, base, dict)
        if dict.get('abstract'):
            return cls
        cls.setUpAttr()
        for nd in cls.get_data_lists():
            data = getattr(cls, nd, False)
            if data is False:
                raise Exception('Not data for request')
            for i in range(len(data)):
                test_name = "test_%s_request_%s" % (nd, i)
                setattr(cls, test_name, mcs.create_a_function(**data[i]))
        return cls


class BaseTestCase(TestCase):
    """
    Class with  dynamic generated test
    Get data from list with format:
        {'json':{...},      -- args for client (request api)
         'except':{...},    -- expected result (default 200 & json)
         'mock'[{...}]}     -- put mock objects before request
    Default data list - good_data & wrong_name (set this in data_lists)
    """
    __metaclass__ = MetaTestMixin

    url = '/'
    method = 'GET'
    json = {}
    requests = []
    data_lists = ['requests']

    def client(self, **kwargs):
        """
        basic client
        :return: response
        """
        kwargs.update(self.get_client_kwargs())
        json = kwargs.pop('json', {})
        return Client(self.method, self.url,
                      json=json, **kwargs)

    def put_mock(self):
        """
        make function for put mock
        """
        pass

    def base_request(self, **kwargs):
        return None

    @classmethod
    def setUpAttr(cls):
        """
        set attributes for generic test class before run test
        """
        pass

    def get_client_kwargs(self):
        """
        adding kwargs to client
        :return:
        """
        return {}

    @classmethod
    def get_data_lists(self):
        """
        :return: list with names for tests request data
        """
        return self.data_lists