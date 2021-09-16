from fos_api_prom_exporter.fos_api import PrometheusFOSAPIInterface
import json

URL = "/monitor/vpn/ipsec"

fos = PrometheusFOSAPIInterface()
success, data = fos.get_url(url=URL)

print(success)
print(json.dumps(data, indent=4))
