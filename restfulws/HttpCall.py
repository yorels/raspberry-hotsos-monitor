import http.client
import time
import json
from collections import namedtuple
from commons.BusinessException import HotSOSError
from commons import Settings


IMMUTABLE_OBJECT_FIELDS = [
    'method',
    'url',
    'headers',
    'body'
]


class RequestBuilder(object):

    def __init__(self, required_http_method, required_http_url, http_headers=None, http_body=None):
        self.method = required_http_method
        self.url = required_http_url
        self.headers = http_headers
        self.body = http_body

    def build(self):
        return ImmutableObject(self.method,
                               self.url,
                               self.headers,
                               self.body,
                               )


class ImmutableObject(namedtuple('ImmutableObject', IMMUTABLE_OBJECT_FIELDS)):
    __slots__ = ()

    def __str__(self) -> str:
        return "{\"url\": \"" + self.http_url + "\"," \
            " \"http_method\": \"" + self.http_method + "\"," \
            " \"conversation-Id\": \"" + Settings.token + "\"," \
            " \"user\": \"" + Settings.login + "\"," \
            " \"domain\": \"" + self.headers['domain'] + "\"}"

    @property
    def http_method(self):
        return self.method

    @property
    def http_url(self):
        return self.url

    @property
    def http_headers(self):
        return self.headers

    @property
    def http_body(self):
        return self.body


class HttpCall(object):

    response = {
        'url': '',
        'status_code': '',
        'reason': '',
        'domain': '',
        'conversation-Id': '',
        'user': '',
        'time_spent': '',
        'response': ''
    }

    def __init__(self, request):
        self.request = request

    def call(self) -> response:
        ts = time.time()
        conn = ()

        try:
            conn = http.client.HTTPSConnection(Settings.hot_sos_host)
            conn.request(self.request.http_method, self.request.http_url, self.request.http_body,
                         self.request.http_headers)
            self.response['time_spent'] = '{0:.5f} ms'.format((time.time() - ts) * 1000)

            res = conn.getresponse()
            status_code = res.getcode().__str__()
            self.response['url'] = self.request.http_url
            self.response['status_code'] = status_code
            self.response['reason'] = res.reason
            self.response['domain'] = Settings.hot_sos_host
            self.response['conversation-Id'] = Settings.token
            self.response['user'] = Settings.login
            self.response['response'] = res.read().decode('utf-8')

            if res.getheader('Set-Cookie'):
                Settings.auth = res.getheader('Set-Cookie')

            if status_code == '200':
                pass
            else:
                raise Exception(json.dumps(self.response))
        except Exception as exc:
            raise HotSOSError(exc.__str__(), exc)
        finally:
            conn.close()
        return self.response
