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

    def get_url(self, host=None, apikey=None, url=None, vdom=None, filter=None):
        """ Gets and returns a URL from a Fortigate based on its class self.* properties"""
        if not host:
            host = self.fos_host
        if not apikey:
            apikey = os.environ.get("FOS_API_KEY")
        with pyFGT.fortigate.FortiGate(host,
                                       apikey=apikey,
                                       use_ssl=self.fos_use_ssl,
                                       debug=self.fos_debug,
                                       verify_ssl=self.fos_verify_ssl,
                                       disable_request_warnings=self.fos_disable_request_warnings,
                                       timeout=int(self.fos_polling_timeout)) as fgt:
            ret = ["pending"]
            if not vdom:
                vdom = "root"
            if filter:
                ret = fgt.get(url, f"vdom={vdom}", f"filter={filter}")
            elif not filter:
                ret = fgt.get(url, f"vdom={vdom}")
            if ret[0] == "success":
                return True, ret[1]
            else:
                return False, ret
