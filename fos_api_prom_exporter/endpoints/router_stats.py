from prometheus_client import Counter, Gauge, Enum, Summary, Histogram, Info
from fos_api_prom_exporter.endpoints.base import FOSEndpoint


class RouterStatistics(FOSEndpoint):
    def __init__(self):
        self.url = "/monitor/router/statistics"
        super(RouterStatistics, self).__init__()

    def init_prom_metrics(self):
        self.prom_metrics = {
            "routes": Gauge('fgt_routes', 'Total number of routes'),
            "ipv4_routes": Gauge('fgt_ipv4_routes', 'Total number of IPv4 routes'),
            "ipv6_routes": Gauge('fgt_ipv6_routes', 'Total number of IPv6 routes')
        }

    def update_prom_metrics(self):
        results = dict(self.url_results["results"])
        for k, v in results.items():
            try:
                if k == "total_lines":
                    self.prom_metrics["routes"].set(v)
                if k == "total_lines_ipv4":
                    self.prom_metrics["ipv4_routes"].set(v)
                if k == "total_lines_ipv6":
                    self.prom_metrics["ipv6_routes"].set(v)
            except Exception as e:
                self.logs.error(f"Error updating metric {k}: {e}")
                continue
        self.logs.debug(f"Done Updating Prom Metrics for {__name__}")


