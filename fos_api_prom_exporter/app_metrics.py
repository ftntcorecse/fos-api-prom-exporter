from prometheus_client import Histogram

# create a specific metric for logging how long it takes to get data from the FortiGate
WHOLE_COLLECTION_DURATION = Histogram('fos_metric_collection_duration',
                                      'How long it takes for each collection pass on the fortigate')
# create a metric for the polling saturation
POLLING_INTERVAL_SATURATION = Histogram('fos_metric_polling_interval_saturation',
                                        'A KPI for how long it takes to query the FortiGate API compared'
                                        'to how much of the polling interval that time is consuming.')