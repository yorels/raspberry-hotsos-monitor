#import sys
import yaml
import secrets

#sys.path.append('/opt/settings')
with open("/opt/settings/config.yaml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile)

cookie = cfg['default']['cookie']
token = secrets.token_urlsafe()

ud_id = cfg['device']['id']
device_name = cfg['device']['name']

hot_sos_host = cfg['hot_sos']['url']
login = cfg['hot_sos']['login']
password = cfg['hot_sos']['password']
origin = cfg['hot_sos']['origin']

wlan_iface = cfg['wlan']

headers = {
    'cookie': cookie,
    'host': hot_sos_host,
    'origin': origin,
    'content-type': "application/json",
    'Connection': "keep-alive",
}


