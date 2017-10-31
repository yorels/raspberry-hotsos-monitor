import logging
import subprocess
from commons import Settings


class IwQaScanner(object):

    def scan(self):
        cmd = subprocess.Popen('iwconfig %s' % Settings.w_interface, shell=True, stdout=subprocess.PIPE)
        for line in cmd.stdout:
            if 'Link Quality' in line:
                print(line.lstrip(' '))
            elif 'Not-Associated' in line:
                print("No signal")