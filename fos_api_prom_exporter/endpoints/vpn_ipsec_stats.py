from prometheus_client import Counter, Gauge, Enum, Summary, Histogram, Info
from fos_api_prom_exporter.endpoints.base import FOSEndpoint
from os import environ
from os import environ
from dotenv import load_dotenv

load_dotenv()


class VPNIPSecStatistics(FOSEndpoint):
    """Gets the IPSec Tunnel Stats for a FortiGate"""
    def __init__(self):
        self.host = environ.get("FOS_HOST")
        self.url = "/monitor/vpn/ipsec"
        self.vdom = environ.get("FOS_HOST_VDOM")
        self.filter = None
        super(VPNIPSecStatistics, self).__init__()

    def init_prom_metrics(self):
        self.prom_metrics = {
            "ipsec_vpn_tunnels": Gauge('fgt_ipsec_vpn_tunnels',
                                       'Number of IPSec VPN Tunnels', ['host', 'vdom']),
            "ipsec_vpn_connections": Gauge('fgt_ipsec_vpn_connections',
                                           'Number of IPSecVPN Connections', ['host', 'vdom', 'vpn']),
            "ipsec_vpn_inbound_bytes": Gauge('fgt_ipsec_vpn_inbound_bytes',
                                             'Inbound IPSec VPN Bytes', ['host', 'vdom', 'vpn']),
            "ipsec_vpn_outbound_bytes": Gauge('fgt_ipsec_vpn_outbound_bytes',
                                              'Outbound IPSec VPN Bytes', ['host', 'vdom', 'vpn']),
        }

    def update_prom_metrics(self, host=None, vdom=None, results=None):
        vpn_tunnels = 0
        for vpn_tunnel in results["results"]:
            try:
                vpn_tunnels += 1
                self.prom_metrics["ipsec_vpn_connections"].labels(
                    host=host, vdom=vdom, vpn=vpn_tunnel["name"]).set(vpn_tunnel["connection_count"])
                self.prom_metrics["ipsec_vpn_inbound_bytes"].labels(
                    host=host, vdom=vdom, vpn=vpn_tunnel["name"]).set(vpn_tunnel["incoming_bytes"])
                self.prom_metrics["ipsec_vpn_outbound_bytes"].labels(
                    host=host, vdom=vdom, vpn=vpn_tunnel["name"]).set(vpn_tunnel["outgoing_bytes"])
            except Exception as e:
                self.logs.error(f"Error updating metric {k}: {e}")
                continue
        self.prom_metrics["ipsec_vpn_tunnels"].labels(
            host=host, vdom=vdom).set(vpn_tunnels)
        self.logs.debug(f"Done Updating Prom Metrics for {__name__} on {host}")
