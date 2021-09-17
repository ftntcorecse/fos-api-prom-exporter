import logging, sys
import os
import time
import asyncio
from fos_api_prom_exporter.build_prom_registry import build_prometheus_registry
from fos_api_prom_exporter.collect_endpoints import collect_active_endpoint_monitors
from fos_api_prom_exporter.app_metrics import WHOLE_COLLECTION_DURATION, POLLING_INTERVAL_SATURATION
from fos_api_prom_exporter.get_fgt_list import get_fortigate_list
from prometheus_client import start_http_server

# configure logging
logging.basicConfig(stream=sys.stdout,
                    level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logs = logging.getLogger("FOS_Prometheus_Exporter")

# make asyncio loop
event_loop = asyncio.get_event_loop()

# get any extra fortigates from the env file and store in a dictionary for later use
# these are in addition to the FOS_HOST and FOS_API_KEY values defined in .env
fortigate_list = get_fortigate_list()

# build the prometheus metric registry
REGISTRY = build_prometheus_registry()
# also register the metrics contained in fos_api_prom_exporter.app_metrics that were imported above
REGISTRY.register(WHOLE_COLLECTION_DURATION)
REGISTRY.register(POLLING_INTERVAL_SATURATION)

if __name__ == '__main__':
    server_start_time = time.time()
    # start the prometheus http server
    start_http_server(int(os.environ.get("PROM_EXPORTER_PORT")))
    logs.info(f"Prometheus Server started on port {os.environ.get('PROM_EXPORTER_PORT')}")
    logs.info(f"Periodic heartbeat log messages will be sent.")
    # read the polling interval, so we don't have to keep doing it
    polling_interval = float(os.environ.get("FOS_POLLING_INTERVAL"))
    # init a counter so we can leave heartbeat log messages every so often
    loop_count = 0
    # get the heartbeat modulo from the env vars
    heartbeat_modulo = int(os.environ.get("FOS_HEARTBEAT_MODULO"))
    while True:
        loop_count += 1
        # start a time for this loop
        start_time = time.time()
        # run the collections in async -- include the event loop and extra fortigate list.
        event_loop.run_until_complete(collect_active_endpoint_monitors(event_loop=event_loop,
                                                                       fortigate_list=fortigate_list))
        # record end time
        end_time = time.time()
        # calculate the duration of the collection
        duration = float(end_time - start_time)
        # calculate the polling interval delta (minus duration)
        polling_interval_delta = float(polling_interval - duration)
        # calculate the polling saturation percentage
        polling_saturation = float((duration / polling_interval_delta)*100)
        logs.debug(f"Collection took {duration} seconds.")
        logs.debug(f"Sleeping for {polling_interval_delta} seconds.")
        logs.debug(f"Polling Saturation is {int(polling_saturation)}%")
        # record the duration
        WHOLE_COLLECTION_DURATION.observe(duration)
        # record the polling saturation
        POLLING_INTERVAL_SATURATION.observe(polling_saturation)
        # if the loop count is a modulus of 10, send a heartbeat info log message
        if loop_count % heartbeat_modulo == 0:
            server_start_time_delta = (int(time.time() - server_start_time)/60)
            logs.info(f"FortiOS Prometheus Exporter has sampled {loop_count} times "
                      f"in {round(server_start_time_delta, 1)} minutes or {round(server_start_time_delta/60, 2)} hours "
                      f"or {round(server_start_time_delta/60/24,3)} days.")
        # sleep -- back off if the delta is negative (polling saturation > 100%)
        if polling_interval_delta < 0:
            logs.warning("Polling interval exceeded! Sleeping for 15 seconds. We cannot sleep for negative seconds.")
            logs.error("This exporter requires tuning. It's polling interval is being exceeded during collection.")
            time.sleep(15)
        else:
            time.sleep(polling_interval_delta)
