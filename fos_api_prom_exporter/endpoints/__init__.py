from fos_api_prom_exporter.endpoints.system import SystemResourceUsage
from fos_api_prom_exporter.endpoints.router_stats import RouterStatistics
from fos_api_prom_exporter.endpoints.vpn_ssl_stats import VPNSSLStatistics
from fos_api_prom_exporter.endpoints.status import Status
from fos_api_prom_exporter.endpoints.interfaces import Interfaces

ACTIVE_ENDPOINT_MONITORS = {
    # "systemResourceUsage": SystemResourceUsage(),
    # "routerStatistics": RouterStatistics(),
    # "vpnSSLStatistics": VPNSSLStatistics(),
    # "status": Status(),
    "interfaces": Interfaces()
}