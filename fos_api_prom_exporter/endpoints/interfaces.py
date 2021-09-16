from prometheus_client import Counter, Gauge, Enum, Summary, Histogram, Info
from fos_api_prom_exporter.endpoints.base import FOSEndpoint
from os import environ
from dotenv import load_dotenv

load_dotenv()


class Interfaces(FOSEndpoint):
    def __init__(self):
        self.url = "/monitor/system/interface"
        self.vdom = environ.get("FOS_HOST_VDOM")
        self.filter = "include_vlan==true"
        super(Interfaces, self).__init__()

    def init_prom_metrics(self):
        self.prom_metrics = {
            "interface_rx_bytes": Histogram('fgt_interface_rx_bytes', 'Total inbound bytes to all interfaces')
        }

    def update_prom_metrics(self):
        results = dict(self.url_results["results"])
        rx_bytes = []
        for k, v in results.items():
            try:
                rx_bytes.append(v["rx_bytes"])
            except Exception as e:
                self.logs.error(f"Error updating metric {k}: {e}")
                continue
        rx_bytes_sum = sum(rx_bytes)
        self.prom_metrics["interface_rx_bytes"].observe(rx_bytes_sum)

        self.logs.debug(f"Done Updating Prom Metrics for {__name__}")

