from prometheus_client import Counter, Gauge, Enum, Summary, Histogram, Info
from fos_api_prom_exporter.endpoints.base import FOSEndpoint


class VPNSSLStatistics(FOSEndpoint):
    def __init__(self):
        self.url = "/monitor/vpn/ssl/stats"
        super(VPNSSLStatistics, self).__init__()

    def init_prom_metrics(self):
        self.prom_metrics = {
            "sslvpn_max_users": Gauge('fgt_sslvpn_max_users',
                                      'Max number of SSLVPN Users seen'),
            "sslvpn_max_tunnels": Gauge('fgt_sslvpn_max_tunnels',
                                        'Max number of SSLVPN Tunnels seen'),
            "sslvpn_max_connections": Gauge('fgt_sslvpn_max_connections',
                                            'Max number of SSLVPN Connections seen'),
            "sslvpn_current_users": Gauge('fgt_sslvpn_current_users',
                                          'Current number of SSLVPN Users seen'),
            "sslvpn_current_tunnels": Gauge('fgt_sslvpn_current_tunnels',
                                            'Current number of SSLVPN Tunnels seen'),
            "sslvpn_current_connections": Gauge('fgt_sslvpn_current_connections',
                                                'Current number of SSLVPN Connections seen'),
            "fgt_conserve_mode": Info('fgt_conserve_mode', 'Conserve mode status')
        }

    def update_prom_metrics(self):
        results = dict(self.url_results["results"])
        for k, v in results.items():
            try:
                if k == "conserve_mode":
                    self.prom_metrics["fgt_conserve_mode"].info({"conserve_mode": str(v)})
                if k == "max":
                    self.prom_metrics["sslvpn_max_users"].set(v["users"])
                    self.prom_metrics["sslvpn_max_tunnels"].set(v["tunnels"])
                    self.prom_metrics["sslvpn_max_connections"].set(v["connections"])
                if k == "current":
                    self.prom_metrics["sslvpn_current_users"].set(v["users"])
                    self.prom_metrics["sslvpn_current_tunnels"].set(v["tunnels"])
                    self.prom_metrics["sslvpn_current_connections"].set(v["connections"])
            except Exception as e:
                self.logs.error(f"Error updating metric {k}: {e}")
                continue
        self.logs.debug(f"Done Updating Prom Metrics for {__name__}")


