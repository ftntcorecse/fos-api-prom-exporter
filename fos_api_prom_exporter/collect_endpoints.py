from fos_api_prom_exporter.endpoints import ACTIVE_ENDPOINT_MONITORS


def collect_active_endpoint_monitors():
    for name, monitor in ACTIVE_ENDPOINT_MONITORS.items():
        monitor.logs.debug(f"Fetching Monitor {name}")
        monitor.collect()
