from fos_api_prom_exporter.endpoints import ACTIVE_ENDPOINT_MONITORS
import asyncio

# event_loop = asyncio.get_event_loop()


async def collect_active_endpoint_monitors(event_loop):
    task_list = []
    for name, monitor in ACTIVE_ENDPOINT_MONITORS.items():
        monitor.logs.debug(f"Fetching Monitor {name}")
        task = event_loop.create_task(monitor.collect())
        task_list.append(task)
    await asyncio.wait(task_list)
