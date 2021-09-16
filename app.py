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
POLLING_INTERVAL_SAUTRATION = Histogram('fos_metric_polling_interval_saturation',
                                        'A KPI for how long it takes to query the FortiGate API compared'
                                        'to how much of the polling interval that time is consuming.')

REGISTRY = build_prometheus_registry()
REGISTRY.register(WHOLE_COLLECTION_DURATION)

if __name__ == '__main__':
    start_http_server(int(os.environ.get("PROM_EXPORTER_PORT")))
    logs.info(f"Prometheus Server started on port {os.environ.get('PROM_EXPORTER_PORT')}")
    polling_interval = int(os.environ.get("FOS_POLLING_INTERVAL"))
    while True:
        start_time = time.time()
        # run the collections in async
        event_loop.run_until_complete(collect_active_endpoint_monitors(event_loop))
        # record end time
        end_time = time.time()
        # report total time taken and the polling interval delta
        duration = float(end_time - start_time)
        polling_interval_delta = float(polling_interval - duration)
        polling_saturation = float((duration / polling_interval_delta)*100)
        logs.info(f"Collection took {duration} seconds.")
        logs.info(f"Sleeping for {polling_interval_delta} seconds.")
        logs.info(f"Polling Saturation is {int(polling_saturation)}%")
        # record the duration
        WHOLE_COLLECTION_DURATION.observe(duration)
        POLLING_INTERVAL_SAUTRATION.observe(polling_saturation)
        # sleep -- back off if the delta is negative
        if polling_interval_delta < 0:
            logs.warning("Polling interval exceeded! Sleeping for 5 seconds.")
            time.sleep(5)
        else:
            time.sleep(polling_interval_delta)
