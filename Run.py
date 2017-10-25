import logging
from time import time
from commons.BusinessException import HotSOSError
from monitors.Monitors import Monitors


#Pending integration with WiFi monitor
class Run(object):

    @staticmethod
    def main():
        ts = time()
        logger = logging.getLogger('monitor')

        try:
            logging.info(Monitors().run_monitors())
        except HotSOSError as err:
            logger.error(err.__str__())
        except Exception as e:
            logger.error(e, exc_info=True)
        finally:
            logger.info("Took %s seconds", (time() - ts))


if __name__ == '__main__':
    Run.main()
