from abc import ABC, abstractmethod
from dotenv import load_dotenv
import os, logging, sys
from fos_api_prom_exporter.fos_api import PrometheusFOSAPIInterface
import asyncio

logging.basicConfig(stream=sys.stdout,
                    level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


class FOSEndpoint(ABC):
    """
    A base abstract class that represents and contains the needed metadata and prometheus metrics.
    Inherited by other endpoint modules using super().
    One new child class per URL endpoint. That URL endpoint may yield many metrics, but it is a 1:1 relationship.

    Please see endpoints/system.py for a fully documented example.

    When inherited you must define these values (again, see endpoints/system.py for an example):

    self.url
    self.host
    self.vdom
    self.filter

    When inherited you must write specific functions for the URL endpoint selected, and they will vary greatly:
        init_prom_metrics() -  creates the prometheus metrics objects with labels. almost must include labels.
        update_prom_metrics() - takes the results from a GET url call and parses them to their appropriate prometheus
                                metrics created in init_prom_metrics().
    Please see the other .py files in this "endpoints" directory for examples on how this class is inherited
    and written for specific URL endpoints.
    """
    def __init__(self):
        # load the .env file -- which should always be on git ignore, but always added to docker builds.
        # see .env.example for more info.
        load_dotenv()
        # create the logger
        self.logs = logging.getLogger(__name__)
        # load the pyFGT interface
        self.fgt = PrometheusFOSAPIInterface()
        # load the .env polling interval
        self.polling_interval = os.environ.get("FOS_POLLING_INTERVAL")
        # placeholder
        self.url_results = None
        # prom metrics placeholder. To be overwritten.
        self.prom_metrics = None
        # init the prom metrics function to create prometheus metrics.
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
    def vdom(self):
        return self.__vdom

    @vdom.setter
    def vdom(self, vdom=""):
        self.__vdom = vdom

    @property
    def filter(self):
        return self.__filter

    @filter.setter
    def filter(self, filter=""):
        self.__filter = filter

    @property
    def host(self):
        return self.__host

    @host.setter
    def host(self, host=""):
        self.__host = host

    @property
    def prom_metrics(self):
        return self.__prom_metrics

    @prom_metrics.setter
    def prom_metrics(self, prom_metrics=""):
        self.__prom_metrics = prom_metrics

    async def collect(self, host=None, apikey=None, vdom=None):
        """ Called by collect_endpoints.py -- an async function used by app.py (the main HTTP app/entrypoint).
        When other classes inherit this one they automatically have this called,
        when the app.py does its polling interval.
        This depends on the two abstract functions below being re-written in the child class (see below).
        """
        # if FOS_EXTRA_HOST_x parameters were not passed, then use the default FOS_HOST and FOS_VDOM
        # the APIKEY will be pulled from environment variables in the fos_api.py interface
        # if the apikey is not included here.
        if not host:
            host = self.host
        if not vdom:
            vdom = self.vdom
        try:
            success, data = self.fgt.get_url(host=host,
                                             apikey=apikey,
                                             url=self.url,
                                             vdom=vdom,
                                             filter=self.filter)
            if success:
                # if successful in retrieving the data, then make a copy into a new dictionary
                # and send that dictionary, along with the host/vdom called, to the update_prom_metrics
                # class that has been abstracted in the child endpoint module.
                results = dict(data)
                self.update_prom_metrics(host=host, vdom=vdom, results=results)
            else:
                raise ConnectionError(f"The call to url {self.url} failed.")
        except Exception as e:
            self.logs.error(f"An error occurred collecting some metrics on {host}: {e})")

    @abstractmethod
    def init_prom_metrics(self):
        """An Abstracted class responsible for creating Prometheus metrics and assigning to self.prom_metrics.
        Always remember to include labels as the third argument to a prometheus metric object.
        This way when metrics are recording, they can be differentiated by FortiGate host, and VDOM, and
        in this case, interfaces as well. This is important for Grafana usage.

        Example child abstract class should run something like this:

        self.prom_metrics = {
            "interface_rx_bytes": Histogram('fgt_interface_rx_bytes',               # note the labels here below
                                            'Total inbound bytes to interfaces', ['host', 'interface', 'vdom']),
            "interface_tx_bytes": Histogram('fgt_interface_tx_bytes',
                                            'Total outbound bytes to interfaces', ['host', 'interface', 'vdom']),
            "interface_rx_packets": Histogram('fgt_interface_rx_packets',
                                              'Total inbound packets to interfaces', ['host', 'interface', 'vdom'])
                          }

        """
        raise NotImplementedError("This class should be abstracted!")

    @abstractmethod
    def update_prom_metrics(self, host=host, vdom=vdom, results=None):
        """An abstracted method that takes the results from a URL call and updates the list of metrics
        created above in init_prom_metrics().

        Example of how to update those metrics:

        self.prom_metrics["interface_rx_bytes"].labels(host=host,
                                                       interface=v["name"],
                                                       vdom=vdom).observe(v["rx_bytes"])

        Note the usage of .labels(key=value) immediately after the prometheus metric itself, and THEN we "observe"
        the data (observe is specific to a histogram, could be any number of operations).

        """
        raise NotImplementedError("This class should be abstracted!")

