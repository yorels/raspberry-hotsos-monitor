import logging
from commons import Settings
from multiprocessing import util
from network import IWQAScanner
from restfulws.EndPoint import EndPointOperations


logger = logging.getLogger(__name__)


class Monitors(object):

    headers = Settings.headers

    def __init__(self, with_caching=True):
        if not with_caching:
            self.headers['Cache-Control'] = "no-cache, no-store, must-revalidate"
            self.headers['Pragma'] = "no-cache"
            self.headers['Expires'] = "0"

    def run_monitors(self, **kwargs) -> str:

        if kwargs.get("verbose"):
            logger.setLevel(util.DEBUG)

        if kwargs.get("wifi"):
            logger.debug("WiFi signal monitor: ON, interface:" + Settings.w_interface )
            IWQAScanner.iwlist()

        self.login_monitor()
        self.headers['cookie'] = Settings.cookie + "; " + Settings.auth
        self.is_person_on_duty_monitor()
        self.set_person_off_duty()
        self.list_messages_thread_info_monitor()
        self.unread_message_count_monitor()
        self.standards_for_user_monitor()
        return "Success!"

    def login_monitor(self):
        payload = "{'login':'" + Settings.login + "'" \
            ",'password':'" + Settings.password + "'" \
            ",'udid':'""'" \
            ",'token':'""'}"
        res = EndPointOperations().consume('POST', '/hotsos/rpc/Auth/LoginWithPassword', self.headers, payload)
        logger.debug(res)

    def is_person_on_duty_monitor(self):
        res = EndPointOperations().consume('POST', '/hotsos/rpc/Person/IsPersonOnDuty', self.headers, None)
        logger.debug(res)

    def current_user_monitor(self):
        res = EndPointOperations().consume('GET', '/hotsos/rpc/Auth/GetCurrentUser', self.headers, None)
        logger.debug(res)

    def set_person_off_duty(self):
        res = EndPointOperations().consume('POST', '/hotsos/rpc/Person/SetPersonOffDuty', self.headers, None)
        logger.debug(res)

    def unread_message_count_monitor(self):
        res = EndPointOperations().consume('POST', '/hotsos/rpc/Message/GetUnreadMessageCount', self.headers, None)
        logger.debug(res)

    def list_messages_thread_info_monitor(self):
        payload = "{'filter':" \
                  "{'messageTypeSO':true,'messageTypeMessages':true,'messageTypeReports':true,'searchTerm':''}," \
                  "'resetFilter':false}"
        res = EndPointOperations().consume('POST', '/hotsos/rpc/Message/GetListMessagesThreadInfo', self.headers, payload)
        logger.debug(res)

    def standards_for_user_monitor(self):
        res = EndPointOperations().consume('POST', '/hotsos/rpc/SO/GetStandardsForUser', self.headers, None)
        logger.debug(res)