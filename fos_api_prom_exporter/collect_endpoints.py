from fos_api_prom_exporter.endpoints import ACTIVE_ENDPOINT_MONITORS
import asyncio


async def collect_active_endpoint_monitors(event_loop=None, fortigate_list=None):
    """ Takes the event_loop generated in app.py -- creates tasks for each endpoint 'collect' method.
        Waits for all of them to finish and then returns.

        Each endpoint class only covers one URL, so this works out.
    """
    task_list = []
    for name, monitor in ACTIVE_ENDPOINT_MONITORS.items():
        monitor.logs.debug(f"Fetching Monitor {name}")
        task = event_loop.create_task(monitor.collect())
        task_list.append(task)
        for fgt in fortigate_list:
            task = event_loop.create_task(monitor.collect(host=fgt["host"],
                                                          apikey=fgt["apikey"],
                                                          vdom=fgt["vdom"]))
            task_list.append(task)

    await asyncio.wait(task_list)
