import sys
import time
import json
import requests
from prometheus_client import start_http_server, Metric, REGISTRY, CollectorRegistry

class JsonCollector(object):
  def __init__(self, endpoint):
    self._endpoint = 'http://' + endpoint + ':8081/analytics/uves/virtual-network/*?flat'

  def collect(self):

    # get metric about control nodes

    url = self._endpoint

    # Fetch the JSON
    response = json.loads(requests.get(url).content.decode('UTF-8'))

    metric = Metric('virtual_networks', 'metrics for virtual network', 'summary')

    for entry in response['value']:
      # get json response from link 
      name = entry['name']
      if ('UveVirtualNetworkAgent' in entry['value'] and (entry['value']['UveVirtualNetworkAgent'].get('in_bandwidth_usage') is not None) ):
        
        # get dict UveVirtualNetworkAgent
        tmp = entry['value']['UveVirtualNetworkAgent']
        metric.add_sample('in_bandwidth_usage', value=entry['value']['UveVirtualNetworkAgent'].get('in_bandwidth_usage'), labels={"id": name})
        metric.add_sample('out_bandwidth_usage', value=entry['value']['UveVirtualNetworkAgent'].get('out_bandwidth_usage'), labels={"id": name})
        metric.add_sample('ingress_flow_count', value=entry['value']['UveVirtualNetworkAgent'].get('ingress_flow_count'), labels={"id": name})
        metric.add_sample('egress_flow_count', value=entry['value']['UveVirtualNetworkAgent'].get('egress_flow_count'), labels={"id": name})
        
        # Export metric
        yield metric


if __name__ == '__main__':
  # Usage python file.py endpoint
  
  registry = CollectorRegistry()
  registry.register(JsonCollector(sys.argv[1]))
  start_http_server(8083, registry=registry)
  #start_http_server(8083)
  #REGISTRY.register(JsonCollector(sys.argv[1]))

  while True: time.sleep(1)
