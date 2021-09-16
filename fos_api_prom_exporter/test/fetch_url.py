from fos_api_prom_exporter.fos_api import PrometheusFOSAPIInterface
import json

"""
Use this tool to get the data structure of any given FortiOS API Endpoint quickly,
 so you can write new endpoint classes.

Only uses FOS_HOST and FOS_API_KEY env vars. EXTRA fgt hosts are not considered.
"""

URL = "/monitor/vpn/ipsec"

fos = PrometheusFOSAPIInterface()
success, data = fos.get_url(url=URL)

print(success)
print(json.dumps(data, indent=4))
