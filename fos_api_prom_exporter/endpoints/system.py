from prometheus_client import Counter, Gauge, Enum, Summary, Histogram, Info
from fos_api_prom_exporter.endpoints.base import FOSEndpoint


class SystemResourceUsage(FOSEndpoint):
    def __init__(self):
        self.url = "/monitor/system/resource/usage"
        super(SystemResourceUsage, self).__init__()

    def init_prom_metrics(self):
        self.prom_metrics = {
            "cpu": Gauge('fgt_cpu_usage', 'CPU Resource Utilization'),
            "mem": Gauge('fgt_memory_usage', 'RAM/Memory Resource Utilization'),
            "disk": Gauge('fgt_disk_usage', 'Disk spaced used percent'),
            "session": Gauge('fgt_ipv4_sessions', 'Active IPv4 Sessions'),
            "session6": Gauge('fgt_ipv6_sessions', 'Active IPv6 Sessions'),
            "setuprate": Gauge('fgt_ipv4_session_setup_rate', 'Rate of new IPv4 Sessions'),
            'setuprate6': Gauge('fgt_ipv6_session_setup_rate', 'Rate of new IPv6 Sessions'),
            "npu_session": Gauge('fgt_ipv4_npu_sessions', 'Active IPv4 Sessions using NPU'),
            "npu_session6": Gauge('fgt_ipv6_npu_sessions', 'Active IPv6 Sessions using NPU'),
            "nturbo_session": Gauge('fgt_ipv4_nturbo_sessions', 'Active IPv4 Sessions using nTurbo'),
            "nturbo_session6": Gauge('fgt_ipv6_nturbo_sessions', 'Active IPv6 Sessions using nTurbo'),
            "disk_lograte": Gauge('fgt_log_rate_disk', 'Rate of log messages written to disk'),
            "faz_lograte": Gauge('fgt_log_rate_faz', 'Rate of log messages written to FortiAnalyzer'),
            "forticloud_lograte": Gauge('fgt_log_rate_forticloud', 'Rate of log messages written to FortiCloud'),
            "fgt_version": Info('fgt_version', 'Firmware running on the FGT'),
            "fgt_version_build": Info('fgt_version_build', 'Specific version build number'),
            "fgt_serial": Info('fgt_serial_number', 'Device Serial Number'),
            "fgt_vdom": Info('fgt_vdom', 'VDOM Being monitored')
        }

    def update_prom_metrics(self):
        results = dict(self.url_results["results"])
        for k, v in results.items():
            try:
                self.prom_metrics[k].set(v[0]["current"])
                self.logs.debug(f"{k}: {v[0]['current']}")
            except Exception as e:
                self.logs.error(f"Error updating metric {k}: {e}")
                continue
        self.logs.debug(f"Done Updating Prom Metrics for {__name__}")



