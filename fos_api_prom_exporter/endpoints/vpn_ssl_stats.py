from prometheus_client import Counter, Gauge, Enum, Summary, Histogram, Info
from fos_api_prom_exporter.endpoints.base import FOSEndpoint
from os import environ
from os import environ
from dotenv import load_dotenv

load_dotenv()


class VPNSSLStatistics(FOSEndpoint):
    """ Gets the SSL VPN stats for a FortiGate"""
    def __init__(self):
        self.host = environ.get("FOS_HOST")
        self.url = "/monitor/vpn/ssl/stats"
        self.vdom = environ.get("FOS_HOST_VDOM")
        self.filter = None
        super(VPNSSLStatistics, self).__init__()

    def init_prom_metrics(self):
        self.prom_metrics = {
            "sslvpn_max_users": Gauge('fgt_sslvpn_max_users',
                                      'Max number of SSLVPN Users', ['host', 'vdom']),
            "sslvpn_max_tunnels": Gauge('fgt_sslvpn_max_tunnels',
                                        'Max number of SSLVPN Tunnels', ['host', 'vdom']),
            "sslvpn_max_connections": Gauge('fgt_sslvpn_max_connections',
                                            'Max number of SSLVPN Connections', ['host', 'vdom']),
            "sslvpn_current_users": Gauge('fgt_sslvpn_current_users',
                                          'Current number of SSLVPN Users', ['host', 'vdom']),
            "sslvpn_current_tunnels": Gauge('fgt_sslvpn_current_tunnels',
                                            'Current number of SSLVPN Tunnels', ['host', 'vdom']),
            "sslvpn_current_connections": Gauge('fgt_sslvpn_current_connections',
                                                'Current number of SSLVPN Connections', ['host', 'vdom']),
            "fgt_conserve_mode": Info('fgt_conserve_mode', 'Conserve mode status', ['host', 'vdom'])
        }

    def update_prom_metrics(self, host=None, vdom=None, results=None):
        for k, v in results["results"].items():
            try:
                if k == "conserve_mode":
                    self.prom_metrics["fgt_conserve_mode"].labels(host=host, vdom=vdom).info({"conserve_mode": str(v)})
                if k == "max":
                    self.prom_metrics["sslvpn_max_users"].labels(host=host, vdom=vdom).set(v["users"])
                    self.prom_metrics["sslvpn_max_tunnels"].labels(host=host, vdom=vdom).set(v["tunnels"])
                    self.prom_metrics["sslvpn_max_connections"].labels(host=host, vdom=vdom).set(
                        v["connections"])
                if k == "current":
                    self.prom_metrics["sslvpn_current_users"].labels(host=host, vdom=vdom).set(v["users"])
                    self.prom_metrics["sslvpn_current_tunnels"].labels(host=host, vdom=vdom).set(v["tunnels"])
                    self.prom_metrics["sslvpn_current_connections"].labels(host=host, vdom=vdom).set(
                        v["connections"])
            except Exception as e:
                self.logs.error(f"Error updating metric {k}: {e}")
                continue
        self.logs.debug(f"Done Updating Prom Metrics for {__name__}")
