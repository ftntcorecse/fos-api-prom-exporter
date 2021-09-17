from prometheus_client import Counter, Gauge, Enum, Summary, Histogram, Info
from fos_api_prom_exporter.endpoints.base import FOSEndpoint
from os import environ
from dotenv import load_dotenv

load_dotenv()


class Interfaces(FOSEndpoint):
    """Gets basic information about Fortigate Interfaces.
        Includes a self.filter to make sure the VLANs are included in the list
    """
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
        for k, v in results["results"].items():
            try:
                # update the metrics using the interface name as the label
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
            except Exception as e:
                self.logs.error(f"Error updating metric {k}: {e}")
                continue

        self.logs.debug(f"Done Updating Prom Metrics for {__name__} on {host}")
