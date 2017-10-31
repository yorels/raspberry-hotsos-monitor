import logging
import json
from commons.BusinessException import HotSOSError
from restfulws.HttpCall import RequestBuilder, HttpCall

logger = logging.getLogger(__name__)


class EndPointOperations(object):

    response = ()

    @staticmethod
    def operation(method, url, headers, body):
        request_builder = RequestBuilder(method, url, headers, body)
        request = request_builder.build()
        try:
            response = HttpCall(request).call()
        except HotSOSError as exc:
            logger.error(exc.traceback)
            return {'reason': 'ERROR'}

        res = response.pop('response')
        logger.info(json.dumps(response))
        return res

    def consume(self, method, url, headers, body) -> response:
        return self.operation(method, url, headers, body)

