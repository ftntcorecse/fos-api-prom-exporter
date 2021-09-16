from fos_api_prom_exporter.endpoints import ACTIVE_ENDPOINT_MONITORS
from prometheus_client import CollectorRegistry


def build_prometheus_registry():
    """ Builds the list of prometheus metrics from all of the included classes in ACTIVE_ENDPOINT_MONITORS"""
    # init the registry
    registry = CollectorRegistry()
    # iterate the active endpoint dictionary
    for name, monitor in ACTIVE_ENDPOINT_MONITORS.items():
        # for each metric on each endpoint, import it
        for prom_name, prom_object in monitor.prom_metrics.items():
            registry.register(prom_object)
    # return the registry
    return registry
