import sys
import time
import json, re
import requests
from prometheus_client import start_http_server, Metric, REGISTRY, CollectorRegistry
from flatten_json import flatten

class JsonCollector(object):
  def __init__(self, endpoint):
    self._endpoint = 'http://' + endpoint + ':8081/analytics/uves/database-node/*?flat'

  def collect(self):

    # get metric about control nodes
    url = self._endpoint

    # Fetch the JSON
    response = json.loads(requests.get(url).content.decode('UTF-8'))
    json_all_dbnode = response['value']
    number_dbnode = len(json_all_dbnode)
    
    # Add metric system_mem_usage_used
    
    metric = Metric('contrail_status', '', 'gauge')
    for i in range(number_dbnode):
      current_json_dbnode = json_all_dbnode[i]['value']
      current_metric = current_json_dbnode['NodeStatus']['process_info']
      for k in range(len(current_metric)):
        metric.add_sample('contrail_status', value = 1, labels = {
            'process_name': current_metric[k]['process_name'],
            'process_state': current_metric[k]['process_state'],
            'last_start_time': current_metric[k]['last_start_time'],
            'database_node': json_all_dbnode[i]['name']
          })
    yield metric

    metric = Metric('database_node_avl', 'List of databases node available', 'gauge')
    for i in range(number_dbnode):
      metric.add_sample('database_node_avl', value = 1, labels = {
        'database_host': json_all_dbnode[i]['name']
        })
    yield metric


if __name__ == '__main__':
  # Usage python file.py port endpoint
  registry = CollectorRegistry()
  registry.register(JsonCollector('10.60.17.231'))
  start_http_server(9105, registry=registry)

  while True: time.sleep(1)
