from fos_api_prom_exporter.endpoints import ACTIVE_ENDPOINT_MONITORS
import asyncio


async def collect_active_endpoint_monitors(event_loop=None, fortigate_list=None):
    """ Takes the event_loop generated in app.py -- creates tasks for each endpoint 'collect' method.
        Waits for all of them to finish and then returns.

        Each endpoint class only covers one URL, so this works out.
    """
    # init an empty task list for asyncio to collect on
    task_list = []
    # loop over every active monitor
    for name, monitor in ACTIVE_ENDPOINT_MONITORS.items():
        monitor.logs.debug(f"Fetching Monitor {name}")
        # create the async task for the FOS_HOST and FOS_API_KEY entry
        task = event_loop.create_task(monitor.collect())
        # record that task to follow up on it later
        task_list.append(task)
        # now loop through any FOS_EXTRA_HOST_x entries and also create those tasks
        # but we specify the host, apikey, and vdom
        # these values are used in the labels in prometheus to differentiate the fortigates
        for fgt in fortigate_list:
            # create the asyncio collect task for an extra fortigate
            task = event_loop.create_task(monitor.collect(host=fgt["host"],
                                                          apikey=fgt["apikey"],
                                                          vdom=fgt["vdom"]))
            # append that task to the list
            task_list.append(task)
    # wait for all the tasks to finish
    await asyncio.wait(task_list)
