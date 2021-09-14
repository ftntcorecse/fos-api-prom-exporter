from fos_api_prom_exporter.endpoints.system import SystemResourceUsage


ACTIVE_ENDPOINT_MONITORS = {
    "systemResourceUsage": SystemResourceUsage(),
}