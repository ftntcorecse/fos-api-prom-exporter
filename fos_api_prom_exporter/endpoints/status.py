from prometheus_client import Counter, Gauge, Enum, Summary, Histogram, Info
from fos_api_prom_exporter.endpoints.base import FOSEndpoint
from os import environ
from dotenv import load_dotenv

load_dotenv()


class Status(FOSEndpoint):
    def __init__(self):
        self.url = "/monitor/system/status"
        self.vdom = environ.get("FOS_HOST_VDOM")
        self.filter = None
        super(Status, self).__init__()

    def init_prom_metrics(self):
        self.prom_metrics = {
            "fgt_model": Info('fgt_model_name', 'Model name of the FGT'),
            "fgt_hostname": Info('fgt_hostname', 'Hostname of the FGT'),
            "fgt_version": Info('fgt_version', 'Firmware running on the FGT'),
            "fgt_version_build": Info('fgt_version_build', 'Specific version build number'),
            "fgt_serial": Info('fgt_serial_number', 'Device Serial Number'),
            "fgt_vdom": Info('fgt_vdom', 'VDOM Being monitored')
        }

    def update_prom_metrics(self):
        results = dict(self.url_results["results"])
        for k, v in results.items():
            try:
                if k == "results":
                    self.prom_metrics["fgt_model"].info({"fgt_model": str(v["model"])})
                    self.prom_metrics["fgt_hostname"].info({"fgt_hostname": str(v["hostname"])})
                if k == "version":
                    self.prom_metrics["fgt_version"].info({"fgt_version": str(v)})
                if k == "build":
                    self.prom_metrics["fgt_version_build"].info({"fgt_version_build": str(v)})
                if k == "serial":
                    self.prom_metrics["fgt_serial"].info({"fgt_serial": str(v)})
                if k == "vdom":
                    self.prom_metrics["fgt_vdom"].info({"fgt_vdom": str(v)})
            except Exception as e:
                self.logs.error(f"Error updating metric {k}: {e}")
                continue
        self.logs.debug(f"Done Updating Prom Metrics for {__name__}")





