from abc import ABC, abstractmethod
from dotenv import load_dotenv
import os, logging, sys
from fos_api_prom_exporter.fos_api import PrometheusFOSAPIInterface

logging.basicConfig(stream=sys.stdout,
                    level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


class FOSEndpoint(ABC):
    def __init__(self):
        load_dotenv()
        self.logs = logging.getLogger(__name__)
        self.fgt = PrometheusFOSAPIInterface()
        self.polling_interval = os.environ.get("FOS_POLLING_INTERVAL")
        self.url_results = None
        self.prom_metrics = None
        self.init_prom_metrics()

    @property
    def polling_interval(self):
        return self.__polling_interval

    @polling_interval.setter
    def polling_interval(self, polling_interval=""):
        self.__polling_interval = polling_interval

    @property
    def url(self):
        return self.__url

    @url.setter
    def url(self, url=""):
        self.__url = url

    @property
    def url_results(self):
        return self.__url_results

    @url_results.setter
    def url_results(self, url_results=""):
        self.__url_results = url_results

    @property
    def prom_metrics(self):
        return self.__prom_metrics

    @prom_metrics.setter
    def prom_metrics(self, prom_metrics=""):
        self.__prom_metrics = prom_metrics

    def collect(self):
        success, data = self.fgt.get_url(self.url)
        if success:
            self.url_results = dict(data)
            self.update_prom_metrics()
        else:
            raise ConnectionError(f"The call to url {self.url} failed.")

    @abstractmethod
    def init_prom_metrics(self):
        self.prom_metrics = {}

    @abstractmethod
    def update_prom_metrics(self):
        raise NotImplementedError("This class should be abstracted!")

