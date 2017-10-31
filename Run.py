import argparse
import logging
import time
from commons.BusinessException import HotSOSError
from monitors.Monitors import Monitors

logger = logging.getLogger("monitor")


class Run(object):

    @staticmethod
    def main():
        parser = argparse.ArgumentParser()
        parser.add_argument("-w", "--wifi", help="monitor wifi signal", action="store_true")
        parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
        args = parser.parse_args()
        start = time.time()

        try:
            Monitors().run_monitors(wifi=args.wifi, verbose=args.verbose)

        except HotSOSError as err:
            logger.error(err.value + err.traceback)
        except Exception as e:
            logger.error(e, exc_inf=True)
        finally:
            logger.info("Took {0:.5f} ms".format((time.time() - start) * 1000))


if __name__ == '__main__':
    Run.main()
