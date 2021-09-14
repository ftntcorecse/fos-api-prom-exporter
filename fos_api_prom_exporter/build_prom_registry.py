from fos_api_prom_exporter.endpoints import ACTIVE_ENDPOINT_MONITORS
from prometheus_client import CollectorRegistry


def build_prometheus_registry():
    registry = CollectorRegistry()
    for name, monitor in ACTIVE_ENDPOINT_MONITORS.items():
        for prom_name, prom_object in monitor.prom_metrics.items():
            registry.register(prom_object)

    return registry
