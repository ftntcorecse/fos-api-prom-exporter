# FortiGate API Prometheus Exporter

## Pre-Requisites

A FortiGate is required at a minimum.

You should also have a Grafana/Prometheus server setup to receive the data. 


## Getting Started

* Clone this repo to a new project in an IDE of your choice.
* Copy the **.env.example** file to a new file called simply **.env**
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

To be written.

## Expanding Monitoring by Creating New Endpoint Classes

To be written.