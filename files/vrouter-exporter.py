import sys
import time
import json
import requests
from prometheus_client import start_http_server, Metric, REGISTRY, CollectorRegistry

class JsonCollector(object):
  def __init__(self, endpoint):
    self._endpoint = 'http://' + endpoint + ':8081/analytics/uves/vrouter/*?flat'

  def collect(self):

    ##
    # get metrics for vrouters from analytics:
    ##
    url = self._endpoint

    # Fetch the JSON
    response = json.loads(requests.get(url).content.decode('UTF-8'))
    #print (response)
  
    metric = Metric('vrouter_metrics',
        'metrics for vrouters', 'summary')

    for entry in response['value']:
      name = entry["name"]
      print (type(entry["value"]))
      if ("VrouterStatsAgent" in entry["value"] and "raw_drop_stats" in entry["value"]["VrouterStatsAgent"]):
        print(1111)
        tmp = entry["value"]["VrouterStatsAgent"]

        drop_stats = tmp["raw_drop_stats"]
        #drop_stats = tmp.get("raw_drop_stats")
        #if (drop_stats is not None):
        for k in drop_stats:
          metric.add_sample('raw_drop_stats_'+k, value=drop_stats[k], labels={"host_id": name})
   
        #flow_rate = tmp["flow_rate"]
        flow_rate = tmp.get("flow_rate")
        for k in flow_rate:
          metric.add_sample('flow_rate_'+k, value=flow_rate[k], labels={"host_id": name})

        phy_if_stats = tmp["raw_phy_if_stats"]
        #print (phy_if_stats)
        phy_if_stats = list(phy_if_stats.values())[0]
        for k in phy_if_stats:
          metric.add_sample('raw_phy_if_stats_'+k, value=phy_if_stats[k], labels={"host_id": name})

        yield metric

  

if __name__ == '__main__':
  # Usage: tf-analytics-exporter.py port endpoint
  registry = CollectorRegistry()
  registry.register(JsonCollector('10.60.17.231'))
  start_http_server(8081, registry=registry)

  while True: time.sleep(1)
