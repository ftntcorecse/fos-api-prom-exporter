from prometheus_client import Counter, Gauge, Enum, Summary, Histogram, Info
from fos_api_prom_exporter.endpoints.base import FOSEndpoint
from os import environ
from dotenv import load_dotenv

load_dotenv()


class SystemResourceUsage(FOSEndpoint):
    """Gets the resource usage for a FortiGate / VDOM """
    def __init__(self):
        # define the host from the .env file
        self.host = environ.get("FOS_HOST")
        # define the URL -- use test/fetch_url.py to figure out which URL to be monitored.
        self.url = "/monitor/system/resource/usage"
        # get the vdom from the .env file
        self.vdom = environ.get("FOS_HOST_VDOM")
        # set a filter here if needed for the GET operation of any URL to the FortiGate as defined in FNDN.
        self.filter = None
        # overlay these attributes on the FOSEndpoint __init__ method by invoking the super() method
        super(SystemResourceUsage, self).__init__()

    def init_prom_metrics(self):
        """
        Defines the Prometheus metrics for this child class of the FOSEndpoint Abstract class.
        - note the usage of the list on each counter -- these lists denote labels.
        - labels are very important and must be used in each child endpoint class created.
        - those labels are pushed at the time of recording a metric value (see below, update_prom_metrics() )
        - the labels allow you to differentiate the FortiGate, VDOM, and other values, in Grafana.
        :return: None
        """
        self.prom_metrics = {

            "cpu": Gauge('fgt_cpu_usage',  # Metric name
                         'CPU Resource Utilization',  # Metric description
                         ['host', 'vdom']),  # Metric labels - Always remember to include at least the host and vdom.
            "mem": Gauge('fgt_memory_usage', 'RAM/Memory Resource Utilization', ['host', 'vdom']),
            "disk": Gauge('fgt_disk_usage', 'Disk spaced used percent', ['host', 'vdom']),
            "session": Gauge('fgt_ipv4_sessions', 'Active IPv4 Sessions', ['host', 'vdom']),
            "session6": Gauge('fgt_ipv6_sessions', 'Active IPv6 Sessions', ['host', 'vdom']),
            "setuprate": Gauge('fgt_ipv4_session_setup_rate', 'Rate of new IPv4 Sessions', ['host', 'vdom']),
            'setuprate6': Gauge('fgt_ipv6_session_setup_rate', 'Rate of new IPv6 Sessions', ['host', 'vdom']),
            "npu_session": Gauge('fgt_ipv4_npu_sessions', 'Active IPv4 Sessions using NPU', ['host', 'vdom']),
            "npu_session6": Gauge('fgt_ipv6_npu_sessions', 'Active IPv6 Sessions using NPU', ['host', 'vdom']),
            "nturbo_session": Gauge('fgt_ipv4_nturbo_sessions', 'Active IPv4 Sessions using nTurbo', ['host', 'vdom']),
            "nturbo_session6": Gauge('fgt_ipv6_nturbo_sessions', 'Active IPv6 Sessions using nTurbo', ['host', 'vdom']),
            "disk_lograte": Gauge('fgt_log_rate_disk', 'Rate of log messages written to disk', ['host', 'vdom']),
            "faz_lograte": Gauge('fgt_log_rate_faz', 'Rate of log messages written to FortiAnalyzer', ['host', 'vdom']),
            "forticloud_lograte": Gauge('fgt_log_rate_forticloud', 'Rate of log messages written to FortiCloud',
                                        ['host', 'vdom']),
            "faz_cloud_lograte": Gauge('fgt_log_rate_faz_cloud', 'Rate of log messages written to FAZ Cloud',
                                       ['host', 'vdom'])
        }

    def update_prom_metrics(self, host=None, vdom=None, results=None):
        """
        Updates the prometheus metrics. In this case it is easy because we've named the objects in the dictionary
        above exactly as they come across in the URL results from the API call.

        So we simply loop through them get the "current" key for each counter that is returned in this API call.

        :param host: the hostname/ip:port of the FortiGate
        :param vdom: the vdom being queried
        :param results: the results from the url call to this specific fortigate on the self.url property/path
        :return: None
        """
        # the results dictionary returned from pyFGT is very dependable, so we can just pull up the results right away.
        for k, v in results["results"].items():
            try:
                # notice the specification of labels using the input parameters to differentiate this metric
                # it is very important that every self.prom_metrics call/update include the .labels() method
                self.prom_metrics[k].labels(host=host, vdom=vdom).set(v[0]["current"])
                # send the data to the debug logger if set to debug.
                self.logs.debug(f"{k}: {v[0]['current']}")
            except Exception as e:
                # report any errors
                self.logs.error(f"Error updating metric {k}: {e}")
                # keep going on to the next metric, this train doesn't stop.
                continue
        # report the end of the loop to the debug logger
        self.logs.debug(f"Done Updating Prom Metrics for {__name__}")
