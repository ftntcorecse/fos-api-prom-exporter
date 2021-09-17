from prometheus_client import Counter, Gauge, Enum, Summary, Histogram, Info
from fos_api_prom_exporter.endpoints.base import FOSEndpoint
from os import environ
from dotenv import load_dotenv

load_dotenv()


class RouterStatistics(FOSEndpoint):
    """Gets simple router statistics regarding the number of routes active on a FortiGate."""
    def __init__(self):
        self.host = environ.get("FOS_HOST")
        self.url = "/monitor/router/statistics"
        self.vdom = environ.get("FOS_HOST_VDOM")
        self.filter = None
        super(RouterStatistics, self).__init__()

    def init_prom_metrics(self):
        self.prom_metrics = {
            "routes": Gauge('fgt_routes', 'Total number of routes', ['host', 'vdom']),
            "ipv4_routes": Gauge('fgt_ipv4_routes', 'Total number of IPv4 routes', ['host', 'vdom']),
            "ipv6_routes": Gauge('fgt_ipv6_routes', 'Total number of IPv6 routes', ['host', 'vdom'])
        }

    def update_prom_metrics(self, host=None, vdom=None, results=None):
        for k, v in results["results"].items():
            try:
                if k == "total_lines":
                    self.prom_metrics["routes"].labels(host=host, vdom=vdom).set(v)
                if k == "total_lines_ipv4":
                    self.prom_metrics["ipv4_routes"].labels(host=host, vdom=vdom).set(v)
                if k == "total_lines_ipv6":
                    self.prom_metrics["ipv6_routes"].labels(host=host, vdom=vdom).set(v)
            except Exception as e:
                self.logs.error(f"Error updating metric {k}: {e}")
                continue
        self.logs.debug(f"Done Updating Prom Metrics for {__name__} on {host}")


