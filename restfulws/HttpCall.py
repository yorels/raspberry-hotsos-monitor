import http.client
from collections import namedtuple
from commons.BusinessException import HotSOSError
from commons.Settings import hot_sos_host, token

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
        output = "{\"url\": \"" + self.http_url + "\"," \
            " \"http_method\": \"" + self.http_method + "\"," \
            " \"conversation-Id\": \"" + token + "\"," \
            " \"host\": \"" + self.headers['host'] + "\" ," \
            " \"origin\": \"" + self.headers['origin'] + "\" ," \
            " \"http_body\": \"" + self.body.__str__() + "\"""}"
        return output

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
        'status_code': '',
        'reason': '',
        'conversation-Id': '',
        'auth': '',
        'response': '',
        'info': '',
    }

    def __init__(self, request, message):
        self.request = request
        self.message = message

    def call(self) -> response:
        conn = http.client.HTTPSConnection(hot_sos_host)
        try:
            conn.request(self.request.http_method, self.request.http_url, self.request.http_body,
                         self.request.http_headers)
            res = conn.getresponse()
            status_code = res.getcode().__str__()
            self.response['status_code'] = status_code
            self.response['reason'] = res.reason
            self.response['conversation-Id'] = token
            self.response['response'] = res.read().decode("utf-8")

            if res.getheader('Set-Cookie'):
                self.response['auth'] = res.getheader('Set-Cookie')

            self.response['info'] = res.info().__str__()
            if status_code == '200':
                pass
            else:
                raise Exception(self.message + ' : ' + self.response.__str__())
        except Exception as exc:
            raise HotSOSError(exc.__str__(), exc)
        finally:
            conn.close()
        return self.response
