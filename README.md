# FortiGate API Prometheus Exporter

## Contents

1. [Pre-Requisites](#pre-requisites)
2. [Getting Started](#getting-started)
3. [Managing the API Monitor List](#managing-the-api-monitor-list)
4. [Expanding Monitoring by Creating New Endpoint Classes](#expanding-monitoring-by-creating-new-endpoint-classes)
5. [Tuning the Prometheus Exporter](#tuning-the-prometheus-exporter)
6. [Appendix A - .env.example file](#appendix-a---envexample-file)
7. [Appendix B - System Endpoint Class Example](#appendix-b---system-endpoint-class-example)

### Pre-Requisites

A FortiGate is required at a minimum.

You should also have a Grafana/Prometheus server setup to receive the data.

### Getting Started

* Clone this repo to a new project in an IDE of your choice.
* Copy the **.env.example** file to a new file named **.env**
* If multiple Fortigates are needed see the "FOS_EXTRA_HOST_x" lines in the .env.example file.
* Create a read-only admin role on the target FortiGate(s).
* On the FortiGate(s), create a read-only API admin using the role above, and record the API key.
    * Make sure to setup the trusted host IP if this a production deployment.
* Replace the **FOS_API_KEY** value in the **.env** file with the new API key.
* Replace the **FOS_HOST** value to the FortiGate that will be monitored
    * If the FortiGate is using any other port than 443 for the admin GUI, this value needs to reflect that.
    * **host:port** format is always preferred -- otherwise port 443 is assumed.
* Start **app.py**
* Confirm the Prometheus exporter is alive on the HTTP port by opening it with a browser  
  and metrics can be viewed.
* Edit your existing Prometheus server config file to include the following stanza:

```yaml
- job_name: 'fortios_exporter'
    scrape_interval: 5s
    metrics_path: /   < -- this is important
    static_configs:
      - targets: [ 'localhost:8000' ] < -- replace if running on remote server or different port
```

* Restart Prometheus.
* Check that the service in Prometheus is running and metrics are being collected.
* Add Prometheus to Grafana as a data source if not already present.

### Managing the API Monitor List

The file **fos_api_prom_exporter/endpoints/__init__.py** includes a basic dictionary for importing endpoint/monitor
classes and including them for processing.

If any module/class is commented out from this list it will not be processed.

This is also where you import and add additional endpoint classes (see below).

```python
ACTIVE_ENDPOINT_MONITORS = {
    "systemResourceUsage": SystemResourceUsage(),
    "routerStatistics": RouterStatistics(),
    "vpnSSLStatistics": VPNSSLStatistics(),
    "status": Status(),
    "interfaces": Interfaces(),
    # "vpnIPSecStatistics": VPNIPSecStatistics()  # <--- disabled
}
```

### Expanding Monitoring by Creating New Endpoint Classes

The file **fos_api_prom_exporter/endpoints/base.py** includes an abstract class for easily expanding the FortiOS
Prometheus Exporter to include additional APIs and Metrics from the FortiGate.

There are six examples of how these are written under the **fos_api_prom_exporter/endpoints** folder. Please examine
these example classes to understand how to construct a new one.

There are two main methods that need to be written for any new endpoint/monitor class:

* init_prom_metrics
* update_prom_metrics

See their descriptions in base.py as well as the other endpoint files to understand how these are created.

In order to know exactly what metrics you want to create, use **test/fetch_url.py**, and the FNDN FortiOS API Explorer
online, to find new API endpoints and explore what data they return. Look for monitor URLs on FNDN that catch attention,
and then explore those APIs if you can use the data into useful metrics.

Once you have identified new KPIs to write, start with **init_prom_metrics()**. Ensure you include the prometheus labels
such as host, and vdom or else you cannot differentiate them.

### Tuning the Prometheus Exporter

The .env variable **FOS_POLLING_INTERVAL** controls how often new asyncio tasks to pull data are created.

The .env variables **FOS_EXTRA_HOST_x** (numbered x) allows you to add additional FortiGates to monitor from this
specific instance of the exporter. Be sure to review the section below about tuning this exporter if this feature is
used.

The file **fos_api_prom_exporter/endpoints/__init__.py** includes a basic dictionary for importing monitor endpoint
classes and including them for processing.

These three basic tuning elements (or "knobs") will vary greatly from deployment to deployment, and so it is up to the
user to properly tune each instance of this exporter.

Remember that multiple docker instances with different .env files can be run for multi-threading purposes.

The KPI for understanding "how behind" the exporter is in its polling of FortiGates, is called the **Polling Interval
Saturation**.

#### Polling Interval Saturation

The **Polling Interval Saturation** is a percentage (0-100%) of how much time it is taking to actually poll all
FortiGates and Active Monitors, vs the polling interval itself.

If the polling interval is 10 seconds, and the time to poll data is 1 second, that would be a 10% saturation. Like any
CPU gear you want to aim for less than 70% to allow for fluctuations.

If at any point the saturation goes over 100% the exporter will "back off" for 5 seconds at minimum, and throw a **
warning** log event. Look for these log entries in Grafana as it they are the "canary in the coal mine" for polling
tuning problems.

These are the "knobs" for each instance of this exporter that allow you to "tune" the exporters performance
to keep the **Polling Interval Saturation** below 70%:

* Polling Interval
* Extra FortiGates
* Number of Active Endpoints

This is an automatically created Prometheus metric, and it can be tracked/alerted from Grafana.

The name of this metric is: **fos_metric_polling_interval_saturation**

This metric is tracked as a whole across all configured FortiGates and Endpoints, and is labeled.

#### Polling Duration

The polling duration is also tracked as an automatic Prometheus metric: **fos_metric_collection_duration**

This metric is tracked as a whole across all configured FortiGates and Endpoints.

### Appendix A - .env.example file

```
PROM_EXPORTER_PORT = 8000
FOS_POLLING_INTERVAL = 15
FOS_POLLING_TIMEOUT = 4
FOS_HOST = "host:port"
FOS_HOST_LABEL = "friendlyName"
FOS_HOST_VDOM = "root"
FOS_USE_SSL = "True"
FOS_VERIFY_SSL = "False"
FOS_API_KEY = "yourFortiGateAPIKeyWithReadOnlyPermissions"
FOS_DEBUG = "False"
FOS_DISABLE_REQUEST_WARNINGS = "True"

# EXTRA FORTIGATES
# Use the prefix "FOS_EXTRA_HOST_x"
# use the _1 and _2 and _3 and so on to suffix specific additional FOS hosts and API keys
# we use a wildcard operator to pull in all env vars with the prefix "FOS_EXTRA_HOST"
# must be the json format as shown, with the exact same key names.
# it's easier to include the host/apikey/vdom in a dict that try to correlate multiple .env vars.
# see the function @ fos_api_prom_exporter/get_fgt_list.py for how this list is compiled.
# then see the function @ fos_api_prom_exporter/collect_endpoints.py to see how the list is used/executed.
FOS_EXTRA_HOST_1 = '{"host": "10.1.1.1:443", "apikey": "123test", "vdom": "root"}'
#FOS_EXTRA_HOST_2 = '{"host": "10.2.1.1:443", "apikey": "123test", "vdom": "root"}'
#FOS_EXTRA_HOST_3 = '{"host": "10.3.1.1:443", "apikey": "123test", "vdom": "root"}'
```

### Appendix B - System Endpoint Class Example

```python
from prometheus_client import Counter, Gauge, Enum, Summary, Histogram, Info
from fos_api_prom_exporter.endpoints.base import FOSEndpoint
from os import environ
from dotenv import load_dotenv

load_dotenv()


class SystemResourceUsage(FOSEndpoint):
    """Gets the resource usage for a FortiGate / VDOM """

    def __init__(self):
        self.host = environ.get("FOS_HOST")
        self.url = "/monitor/system/resource/usage"
        self.vdom = environ.get("FOS_HOST_VDOM")
        self.filter = None
        super(SystemResourceUsage, self).__init__()

    def init_prom_metrics(self):
        """
        Defines the Prometheus metrics for this child-class of the FOSEndpoint Abstract class. 
        - note the usage of the list on each counter
        - these lists define the labels for each metric
        - those labels are then pushed at the time of recording a metric value (see below, update_prom_metrics() )
        :return: None
        """
        self.prom_metrics = {

            "cpu": Gauge('fgt_cpu_usage',  # Metric name
                         'CPU Resource Utilization',  # Metric description
                         ['host', 'vdom']),  # Metric labels
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
        for k, v in results["results"].items():
            try:
                # notice the specification of labels using the input parameters to differentiate this metric
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

```