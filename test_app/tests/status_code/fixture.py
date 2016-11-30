mock = {
    'url': 'api/status_code/',
    'request': {
        'method': 'POST',
        'data': {'arg': 'foo'}
    },
    'response': {
        'data': {'answer': 'bar'}
    }
}

data = [
    {
        'json': {'arg': 'foo'}
    }, {
        'json': {'arg': 404},
        'expect': {
            'status_code': 404,
            'mime_type': 'text/html'
        }
    }
]
