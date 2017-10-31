import logging
import subprocess
from commons import Settings

logger = logging.getLogger(__name__)


class IwQaScanner(object):

    def scan(self)-> False:
        cmd = subprocess.Popen('iwconfig %s' % Settings.w_interface, shell=True, stdout=subprocess.PIPE, encoding='utf-8')
        out = ''
        for line in cmd.stdout:
            out += line
            logger.debug(line)
            if 'Link Quality' in line:
                logger.info(line.lstrip(' ').rstrip('\n'))
                return True
            elif 'Not-Associated' in line:
                logger.error('No signal > ' + out.rstrip('\n'))
        return False

