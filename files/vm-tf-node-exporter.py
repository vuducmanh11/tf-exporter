import sys
import time
import json
import requests
from prometheus_client import start_http_server, Metric, REGISTRY, CollectorRegistry

class JsonCollector(object):
  def __init__(self, endpoint):
    self._endpoint = 'http://' + endpoint + ':8081/analytics/uves/virtual-machine/*?flat'

  def collect(self):

    # get metric about control nodes

    url = self._endpoint

    # Fetch the JSON
    response = json.loads(requests.get(url).content.decode('UTF-8'))
    metric = Metric('vm_on_sdn', 'metrics for VM SDN', 'summary')

    for entry in response['value']:
      name = entry['name']
      if ('VirtualMachineStats' in entry['value']):
        tmp = entry['value']['VirtualMachineStats']
        #print(type(tmp['cpu_stats'][0]))
        print(entry['value']['UveVirtualMachineAgent']['vm_name'])
        for k in tmp['cpu_stats'][0]:
          metric.add_sample('cpu_stats_'+k, value=tmp['cpu_stats'][0][k], labels={"machine_id": name})

        # Export metric
        yield metric



if __name__ == '__main__':
  # Usage python file.py port endpoint
  registry = CollectorRegistry()
  registry.register(JsonCollector('10.60.17.231'))
  start_http_server(8084, registry=registry) 
  while True: time.sleep(1)
