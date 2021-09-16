from prometheus_client import Counter, Gauge, Enum, Summary, Histogram, Info
from fos_api_prom_exporter.endpoints.base import FOSEndpoint
from os import environ
from dotenv import load_dotenv

load_dotenv()


class SystemResourceUsage(FOSEndpoint):
    def __init__(self):
        self.host = environ.get("FOS_HOST")
        self.url = "/monitor/system/resource/usage"
        self.vdom = environ.get("FOS_HOST_VDOM")
        self.filter = None
        super(SystemResourceUsage, self).__init__()

    def init_prom_metrics(self):
        self.prom_metrics = {
            "cpu": Gauge('fgt_cpu_usage', 'CPU Resource Utilization', ['host', 'vdom']),
            "mem": Gauge('fgt_memory_usage', 'RAM/Memory Resource Utilization', ['host', 'vdom']),
            "disk": Gauge('fgt_disk_usage', 'Disk spaced used percent', ['host', 'vdom']),
            "session": Gauge('fgt_ipv4_sessions', 'Active IPv4 Sessions', ['host', 'vdom']),
            "session6": Gauge('fgt_ipv6_sessions', 'Active IPv6 Sessions', ['host', 'vdom']),
            "setuprate": Gauge('fgt_ipv4_session_setup_rate', 'Rate of new IPv4 Sessions', ['host', 'vdom']),
            'setuprate6': Gauge('fgt_ipv6_session_setup_rate', 'Rate of new IPv6 Sessions', ['host', 'vdom']),
            "npu_session": Gauge('fgt_ipv4_npu_sessions', 'Active IPv4 Sessions using NPU', ['host', 'vdom']),
            "npu_session6": Gauge('fgt_ipv6_npu_sessions', 'Active IPv6 Sessions using NPU', ['host', 'vdom']),
            "nturbo_session": Gauge('fgt_ipv4_nturbo_sessions', 'Active IPv4 Sessions using nTurbo', ['host', 'vdom']),
            "nturbo_session6": Gauge('fgt_ipv6_nturbo_sessions', 'Active IPv6 Sessions using nTurbo', ['host', 'vdom']),
            "disk_lograte": Gauge('fgt_log_rate_disk', 'Rate of log messages written to disk', ['host', 'vdom']),
            "faz_lograte": Gauge('fgt_log_rate_faz', 'Rate of log messages written to FortiAnalyzer', ['host', 'vdom']),
            "forticloud_lograte": Gauge('fgt_log_rate_forticloud', 'Rate of log messages written to FortiCloud',
                                        ['host', 'vdom']),
            "faz_cloud_lograte": Gauge('fgt_log_rate_faz_cloud', 'Rate of log messages written to FAZ Cloud',
                                       ['host', 'vdom'])
        }

    def update_prom_metrics(self, host=None, vdom=None, results=None):
        for k, v in results["results"].items():
            try:
                self.prom_metrics[k].labels(host=host, vdom=vdom).set(v[0]["current"])
                self.logs.debug(f"{k}: {v[0]['current']}")
            except Exception as e:
                self.logs.error(f"Error updating metric {k}: {e}")
                continue
        self.logs.debug(f"Done Updating Prom Metrics for {__name__}")
