from fos_api_prom_exporter.fos_api import PrometheusFOSAPIInterface
import json

"""
Use this tool to get the data structure of any given FortiOS API Endpoint quickly,
 so you can write new endpoint classes.

Only uses FOS_HOST and FOS_API_KEY env vars. EXTRA fgt hosts are not considered.

You are looking for KPI metrics, not a long list of routes for example. Count the routes, don't display the routes.

Don't show the traffic, count the traffic types.

Remember we're working with prometheus here, and should mostly be numerical KPI's. The Info() object from
prometheus_client has limitations in practicality. 

"""
# use FNDN API FortiOS Explorer web page to find new endpoints
# you can also introduce filters
URL = "/monitor/vpn/ipsec"

fos = PrometheusFOSAPIInterface()
success, data = fos.get_url(url=URL) # you can add filter= and add a filter=attribute==value style FOS API filter.

print(success)
print(json.dumps(data, indent=4)) # print the data
