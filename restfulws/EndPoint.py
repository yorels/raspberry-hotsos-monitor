import logging
import json
from restfulws.HttpCall import RequestBuilder, HttpCall

logger = logging.getLogger(__name__)


class EndPointOperations(object):

    response = ()

    def operation(self, method, url, headers, body, err_message):
        request_builder = RequestBuilder(method, url, headers, body)
        request = request_builder.build()
        response = HttpCall(request, err_message).call()

        logger.info(request.__str__())
        logger.info(json.dumps(response))
        self.response = response

    def consume(self, method, url, headers, body, err_message) -> response:
        self.operation(method, url, headers, body, err_message)
        return self.response

