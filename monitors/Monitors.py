from commons import Settings
from commons.BusinessException import HotSOSError
from restfulws.EndPoint import EndPointOperations
from network import IWQAScanner


class Monitors(object):

    headers = Settings.headers
    response = ()

    IWQAScanner.iwlist()

    def run_monitors(self) -> str:
        self.status_monitor()

        a = [1, 2, 3]
        for x in a:
            if self.is_device_subscribed_monitor() is True:
                break
            if x == 3:
                raise HotSOSError('Device needs to be subscribed first. Not Able to Subscribe device',
                                  'ud_id:' + Settings.ud_id)
            self.subscribe_device_monitor()

        self.user_login_monitor()
        self.current_user_monitor()
        self.is_person_on_duty_monitor()
        self.list_messages_thread_info_monitor()
        return 'Success!'

    def status_monitor(self):
        self.response = EndPointOperations().consume('GET', '/hotsos/app/index.html', self.headers, None,
                                                     'Unable to reach HotSOS Server')

    def user_login_monitor(self):
        payload = "{'login':'" + Settings.login + "'" \
            ",'password':'" + Settings.password + "'" \
            ",'udid':'" + Settings.ud_id + "'" \
            ",'token':'" + Settings.token + "'}"

        self.response = EndPointOperations().consume('POST', '/hotsos/rpc/Auth/LoginWithPassword',
                                                     self.headers, payload,
                                                     'Authentication Failed. Unable to login with user and password')

    def current_user_monitor(self):
        self.headers['cookie'] = Settings.cookie + "; " + self.response['auth']
        self.response = EndPointOperations().consume('GET', '/hotsos/rpc/Auth/GetCurrentUser',
                                                     self.headers, None,
                                                     'Failure On current_user_monitor')

    def is_person_on_duty_monitor(self):
        self.headers['cookie'] = Settings.cookie + "; " + self.response['auth']
        self.response = EndPointOperations().consume('POST', '/hotsos/rpc/Person/IsPersonOnDuty',
                                                     self.headers, None,
                                                     'Failure On is_person_on_duty_monitor')

    def unread_message_count_monitor(self):
        self.headers['cookie'] = Settings.cookie + "; " + self.response['auth']
        self.response = EndPointOperations().consume('POST', '/hotsos/rpc/Message/GetUnreadMessageCount',
                                                     self.headers, None,
                                                     'Failure On unread_message_count_monitor')

    def list_messages_thread_info_monitor(self):
        self.headers['cookie'] = Settings.cookie + "; " + self.response['auth']
        payload = "{'filter':" \
                  "{'messageTypeSO':true,'messageTypeMessages':true,'messageTypeReports':true,'searchTerm':''}," \
                  "'resetFilter':false}"
        self.response = EndPointOperations().consume('POST', '/hotsos/rpc/Message/GetListMessagesThreadInfo',
                                                     self.headers, payload,
                                                     'Failure On list_messages_thread_info_monitor')

    def subscribe_device_monitor(self):
        payload = "{'login':'" + Settings.login + "'" \
            ",'password':'" + Settings.password + "'" \
            ",'udid':'" + Settings.ud_id + "'" \
            ",'token':'" + Settings.token + "'" \
            ",'name':" + Settings.device_name + "'}"
        try:
            self.response = EndPointOperations().consume('POST', '/hotsos/rpc/Auth/SubscribeDevice',
                                                         self.headers, payload,
                                                         'Failure On subscribe_device_monitor. '
                                                         'Unable to Subscribe device with name:' + Settings.device_name)
        except HotSOSError:
            # do not raise any exception
            pass

    def is_device_subscribed_monitor(self) -> False:
        payload = "{'name':'" + Settings.device_name + "'" \
            ",'udid':'" + Settings.ud_id + "'" \
            ",'token':'" + Settings.token + "'}"

        self.response = EndPointOperations().consume('POST', '/hotsos/rpc/Auth/IsDeviceSubscribed',
                                                     self.headers, payload,
                                                     'Failure On is_device_subscribed_monitor.')
        if self.response['response'] == 'true':
            return True
