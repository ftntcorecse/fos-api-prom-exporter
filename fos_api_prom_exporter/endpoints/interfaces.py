from prometheus_client import Counter, Gauge, Enum, Summary, Histogram, Info
from fos_api_prom_exporter.endpoints.base import FOSEndpoint
from os import environ
from dotenv import load_dotenv

load_dotenv()


class Interfaces(FOSEndpoint):
    def __init__(self):
        self.host = environ.get("FOS_HOST")
        self.url = "/monitor/system/interface"
        self.vdom = environ.get("FOS_HOST_VDOM")
        self.filter = "include_vlan==true"
        super(Interfaces, self).__init__()

    def init_prom_metrics(self):
        self.prom_metrics = {
            "interface_rx_bytes": Histogram('fgt_interface_rx_bytes',
                                            'Total inbound bytes to interfaces', ['host', 'interface', 'vdom']),
            "interface_tx_bytes": Histogram('fgt_interface_tx_bytes',
                                            'Total outbound bytes to interfaces', ['host', 'interface', 'vdom']),
            "interface_rx_packets": Histogram('fgt_interface_rx_packets',
                                              'Total inbound packets to interfaces', ['host', 'interface', 'vdom']),
            "interface_tx_packets": Histogram('fgt_interface_tx_packets',
                                              'Total outbound packets to interfaces', ['host', 'interface', 'vdom']),
            "interface_rx_errors": Histogram('fgt_interface_rx_errors',
                                             'Total inbound errors on interfaces', ['host', 'interface', 'vdom']),
            "interface_tx_errors": Histogram('fgt_interface_tx_errors',
                                             'Total outbound errors on interfaces', ['host', 'interface', 'vdom']),
        }

    def update_prom_metrics(self, host=None, vdom=None, results=None):
        rx_bytes = []
        tx_bytes = []
        rx_packets = []
        tx_packets = []
        rx_errors = []
        tx_errors = []
        for k, v in results["results"].items():
            try:
                self.prom_metrics["interface_rx_bytes"].labels(host=host,
                                                               interface=v["name"],
                                                               vdom=vdom).observe(v["rx_bytes"])
                self.prom_metrics["interface_tx_bytes"].labels(host=host,
                                                               interface=v["name"],
                                                               vdom=vdom).observe(v["tx_bytes"])
                self.prom_metrics["interface_rx_packets"].labels(host=host,
                                                                 interface=v["name"],
                                                                 vdom=vdom).observe(v["rx_packets"])
                self.prom_metrics["interface_rx_packets"].labels(host=host,
                                                                 interface=v["name"],
                                                                 vdom=vdom).observe(v["tx_packets"])
                self.prom_metrics["interface_rx_errors"].labels(host=host,
                                                                interface=v["name"],
                                                                vdom=vdom).observe(v["rx_errors"])
                self.prom_metrics["interface_tx_errors"].labels(host=host,
                                                                interface=v["name"],
                                                                vdom=vdom).observe(v["tx_errors"])
                rx_bytes.append(v["rx_bytes"])
                tx_bytes.append(v["tx_bytes"])
                rx_packets.append(v["rx_packets"])
                tx_packets.append(v["tx_packets"])
                rx_errors.append(v["rx_errors"])
                tx_errors.append(v["tx_errors"])
            except Exception as e:
                self.logs.error(f"Error updating metric {k}: {e}")
                continue
        # add up the totals and just make it another label, so we can more easily create
        # graphs in grafana
        rx_bytes_sum = int(sum(rx_bytes))
        tx_bytes_sum = int(sum(tx_bytes))
        rx_packets_sum = int(sum(rx_packets))
        tx_packets_sum = int(sum(tx_packets))
        rx_errors_sum = int(sum(rx_errors))
        tx_errors_sum = int(sum(tx_errors))
        self.prom_metrics["interface_rx_bytes"].labels(host=host,
                                                       interface="total",
                                                       vdom=vdom).observe(rx_bytes_sum)
        self.prom_metrics["interface_tx_bytes"].labels(host=host,
                                                       interface="total",
                                                       vdom=vdom).observe(tx_bytes_sum)
        self.prom_metrics["interface_rx_packets"].labels(host=host,
                                                         interface="total",
                                                         vdom=vdom).observe(rx_packets_sum)
        self.prom_metrics["interface_rx_packets"].labels(host=host,
                                                         interface="total",
                                                         vdom=vdom).observe(tx_packets_sum)
        self.prom_metrics["interface_rx_errors"].labels(host=host,
                                                        interface="total",
                                                        vdom=vdom).observe(rx_errors_sum)
        self.prom_metrics["interface_tx_errors"].labels(host=host,
                                                        interface="total",
                                                        vdom=vdom).observe(tx_errors_sum)

        self.logs.debug(f"Done Updating Prom Metrics for {__name__} on {host}")
