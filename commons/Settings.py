import yaml
import secrets

with open("conf/config.yaml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile)

cookie = cfg['default']['cookie']
token = secrets.token_urlsafe()
auth = ""

ud_id = cfg['device']['id']
device_name = cfg['device']['name']

hot_sos_host = cfg['hot_sos']['url']
login = cfg['hot_sos']['login']
password = cfg['hot_sos']['password']
origin = cfg['hot_sos']['origin']

w_interface = cfg['wlan']

headers = {
    'cookie': cookie,
    'domain': hot_sos_host,
    'origin': origin,
    'content-type': "application/json",
    'Connection': "keep-alive",
}


