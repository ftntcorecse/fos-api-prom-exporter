from fos_api_prom_exporter.build_prom_registry import build_prometheus_registry
from fos_api_prom_exporter.collect_endpoints import collect_active_endpoint_monitors
from prometheus_client import start_http_server, Histogram
import logging, sys
import os
import time
import asyncio

logging.basicConfig(stream=sys.stdout,
                    level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# make asyncio loop
event_loop = asyncio.get_event_loop()

logs = logging.getLogger("FOS_Prometheus_Exporter")
# create a specific metric for logging how long it takes to get data from the FortiGate
WHOLE_COLLECTION_DURATION = Histogram('fos_metric_collection_duration',
                                      'How long it takes for each collection pass on the fortigate')

REGISTRY = build_prometheus_registry()
REGISTRY.register(WHOLE_COLLECTION_DURATION)

if __name__ == '__main__':
    start_http_server(int(os.environ.get("PROM_EXPORTER_PORT")))
    logs.info(f"Prometheus Server started on port {int(os.environ.get('PROM_EXPORTER_PORT'))}")
    while True:
        start_time = time.time()
        # run the collections in async
        event_loop.run_until_complete(collect_active_endpoint_monitors(event_loop))
        end_time = time.time()
        logs.info(f"Collection took {end_time - start_time} seconds.")
        logs.info(f"Sleeping for {os.environ.get('FOS_POLLING_INTERVAL')} seconds.")
        WHOLE_COLLECTION_DURATION.observe(float(end_time - start_time))
        time.sleep(int(os.environ.get("FOS_POLLING_INTERVAL")))
