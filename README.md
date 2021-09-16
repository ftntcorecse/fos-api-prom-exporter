# FortiGate API Prometheus Exporter

## Pre-Requisites

A FortiGate is required at a minimum.

You should also have a Grafana/Prometheus server setup to receive the data. 


## Getting Started

* Clone this repo to a new project in an IDE of your choice.
* Copy the **.env.example** file to a new file called simply **.env**
* If multiple Fortigates are needed see the "FOS_EXTRA_HOST" lines in the .env.example file.
* Create a read-only admin role in the FortiGate.
* Create a read-only API admin using the role above, and record the API key.
* Replace the **FOS_API_KEY** value in the **.env** file with the new API key.
* Replace the **FOS_HOST** value to the FortiGate that will be monitored

    * If the FortiGate is using any other port than 443 for the admin GUI, this value needs to reflect that.

* Start **app.py**
* Confirm the Prometheus exporter is alive on the HTTP port by opening it with a brower  
  and metrics can be viewed on a browser. 
* Edit your existing Prometheus server config file to include the following stanza:

```yaml
- job_name: 'fortios_exporter'
    scrape_interval: 5s
    metrics_path: /   < -- this is important
    static_configs:
      - targets: ['localhost:8000'] < -- replace if running on remote server or different port
```

* Restart Prometheus.
* Check that the service in Prometheus is running and metrics are being collected.
* Add Prometheus to Grafana as a data source if not already present. 

## Managing the API Monitor List

The file **fos_api_prom_exporter/endpoints/__init__.py** includes a basic dictionary for importing
monitor classes and including them for processing.

If any module/class is commented out from this list it will not be processed:

```python
ACTIVE_ENDPOINT_MONITORS = {
    "systemResourceUsage": SystemResourceUsage(),
    "routerStatistics": RouterStatistics(),
    "vpnSSLStatistics": VPNSSLStatistics(),
    "status": Status(),
    "interfaces": Interfaces(),
    #"vpnIPSecStatistics": VPNIPSecStatistics()
}
```

## Expanding Monitoring by Creating New Endpoint Classes

The file **fos_api_prom_exporter/endpoints/base.py** includes an abstract class for easily 
expanding the FortiOS Prometheus
Exporter to include additional APIs and Metrics from the FortiGate.

There are six examples of how these are written under the **fos_api_prom_exporter/endpoints** folder. Please examine 
these example classes to understand how to construct a new one.

There are two main methods that need to be written for any new monitor class: 

* init_prom_metrics
* update_prom_metrics

See their descriptions in base.py as well as the other endpoint files to understand how these are created.

In order to know exactly what metrics you want to create, use **test/fetch_url.py**, and the FortiOS FNDN API Explorer online,
to find new API endpoints and explore what data they return.

Once you have identified new KPIs to write, start with **init_prom_metrics()**. Ensure you include the prometheus labels
such as host, and vdom or else you cannot differentiate them. 


## Tuning the Prometheus Exporter

The .env variable **FOS_POLLING_INTERVAL** controls how often new tasks to pull data are created. 

The .env variables **FOS_EXTRA_HOST_x** (numbered x) allows you to add additional FortiGates to monitor from this
specific instance of the exporter.

The file **fos_api_prom_exporter/endpoints/__init__.py** includes a basic dictionary for importing
monitor endpoint classes and including them for processing.

These three basic elements will vary greatly from deployment to deployment, and so it is up to the user to properly tune
each instance of this exporter.

The KPI for understanding "how behind" the exporter is in its polling of Fortigates, is called the **Polling Interval Saturation**.

### Polling Interval Saturation

The Polling Interval Saturation is a percentage (0-100%) of how much time it is taking to actually poll all FortiGates
and Active Monitors, vs the polling interval itself.

If the polling interval is 10 seconds, and the time to poll data is 1 second, that would be a 10% saturation.

This is the metric you must use to properly tune the above mentioned "knobs" for each instance of this exporter:

* Polling Interval
* Extra FortiGates
* Number of Active Endpoints.