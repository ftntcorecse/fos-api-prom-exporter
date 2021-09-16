from fos_api_prom_exporter.endpoints.system import SystemResourceUsage
from fos_api_prom_exporter.endpoints.router_stats import RouterStatistics
from fos_api_prom_exporter.endpoints.vpn_ssl_stats import VPNSSLStatistics
from fos_api_prom_exporter.endpoints.status import Status
from fos_api_prom_exporter.endpoints.interfaces import Interfaces
from fos_api_prom_exporter.endpoints.vpn_ipsec_stats import VPNIPSecStatistics

ACTIVE_ENDPOINT_MONITORS = {
    "status": Status(),
    "interfaces": Interfaces(),
    "systemResourceUsage": SystemResourceUsage(),
    "routerStatistics": RouterStatistics(),
    "vpnSSLStatistics": VPNSSLStatistics(),
    "vpnIPSecStatistics": VPNIPSecStatistics()
}