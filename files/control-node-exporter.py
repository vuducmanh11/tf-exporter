import sys
import time
import json
import requests
from prometheus_client import start_http_server, Metric, REGISTRY, CollectorRegistry

class JsonCollector(object):
  def __init__(self, endpoint):
    self._endpoint = 'http://' + endpoint + ':8081/analytics/uves/control-node/*?flat'

  def collect(self):

    # get metric about control nodes

    url = self._endpoint

    # Fetch the JSON
    response = json.loads(requests.get(url).content.decode('UTF-8'))

    metric = Metric('control_node_metrics', 'metrics for control nodes', 'summary')

    for entry in response['value']:
      name = entry['name']
      if ('NodeStatus' in entry['value']):
        tmp = entry['value']['NodeStatus']
        
        system_mem_usage = tmp['system_mem_usage']
        system_cpu_info = tmp['system_cpu_info']
        for k in system_mem_usage:
          if (k == 'node_type'):
            print ('not')
            continue
          print(k,type(k))
          metric.add_sample('system_mem_usage_'+k, value=system_mem_usage[k], labels={"host_name": name})
        
        for k in system_cpu_info:
          metric.add_sample('system_cpu_info_'+k, value=system_cpu_info[k], labels={"host_name": name})  

        # Export metric
        yield metric



if __name__ == '__main__':
  # Usage python file.py port endpoint
  registry = CollectorRegistry()
  registry.register(JsonCollector('10.60.17.231'))
  start_http_server(8082, registry=registry)

  while True: time.sleep(1)
