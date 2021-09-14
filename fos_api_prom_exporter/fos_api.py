import os
import time
import pyFGT.fortigate
from prometheus_client import start_http_server, Gauge, Enum
from dotenv import load_dotenv
from distutils.util import strtobool


class PrometheusFOSAPIInterface():

    def __init__(self):
        load_dotenv()
        self.fos_host = os.environ.get("FOS_HOST")
        self.fos_use_ssl = bool(strtobool(os.environ.get("FOS_USE_SSL")))
        self.fos_verify_ssl = bool(strtobool(os.environ.get("FOS_VERIFY_SSL")))
        self.fos_debug = bool(strtobool(os.environ.get("FOS_DEBUG")))
        self.fos_disable_request_warnings = bool(strtobool(os.environ.get("FOS_DISABLE_REQUEST_WARNINGS")))
        self.fos_polling_timeout = os.environ.get("FOS_POLLING_TIMEOUT")
        # self.fos_api_key = os.environ.get("FOS_API_KEY") # get this key as needed below

    def get_url(self, url=None):
        """ Gets and returns a URL from a Fortigate based on its class self.* properties"""

        with pyFGT.fortigate.FortiGate(self.fos_host,
                                       apikey=os.environ.get("FOS_API_KEY"),
                                       use_ssl=self.fos_use_ssl,
                                       debug=self.fos_debug,
                                       verify_ssl=self.fos_verify_ssl,
                                       disable_request_warnings=self.fos_disable_request_warnings,
                                       timeout=int(self.fos_polling_timeout)) as fgt:
            ret = fgt.get(url)
            if ret[0] == "success":
                return True, ret[1]
            else:
                return False, ret
