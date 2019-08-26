import sys
import time
import json, re
import requests
from prometheus_client import start_http_server, Metric, REGISTRY, CollectorRegistry

class JsonCollector(object):
  def __init__(self, endpoint, uve_type):
    self._node = uve_type
    self._endpoint = []
    for i in range(len(uve_type)):
      self._endpoint.append('http://' + endpoint + ':8081/analytics/uves/' + uve_type[i] +'/*?flat')
    # self._endpoint = 'http://' + endpoint + ':8081/analytics/uves/' + uve_type +'/*?flat'

  def collect(self):

    # get metric about control nodes
    urls = self._endpoint

    metric = Metric('contrail_status', '', 'gauge')

    # Fetch the JSON
    for i in range(len(urls)):

      response = json.loads(requests.get(urls[i]).content.decode('UTF-8'))
      json_all_node = response['value']
      number_node = len(json_all_node)
      
      # Add metric system_mem_usage_used
      
      # metric = Metric('contrail_status', '', 'gauge')
      for i in range(number_node):
        current_json_node = json_all_node[i]['value']
        current_metric = current_json_node['NodeStatus']['process_info']
        for k in range(len(current_metric)):
          metric.add_sample('contrail_status', value = 1, labels = {
              'process_name': current_metric[k]['process_name'],
              'process_state': current_metric[k]['process_state'],
              'last_start_time': current_metric[k]['last_start_time'],
              'node': json_all_node[i]['name'],
              'node_type': re.sub(r'[:-]', '_', self._node[i])
            })
    yield metric
    # Metric
    for i in range(len(urls)):

      response = json.loads(requests.get(urls[i]).content.decode('UTF-8'))
      json_all_node = response['value']
      number_node = len(json_all_node)
      metric = Metric(re.sub(r'[:-]', '_', self._node[i]), 'List of node available', 'gauge')
      for k in range(number_node):
        metric.add_sample(re.sub(r'[:-]', '_', self._node[i]), value = 1, labels = {
          'config_host': json_all_node[k]['name']
          })
      yield metric


if __name__ == '__main__':
  # Usage python file.py port endpoint
  registry = CollectorRegistry()
  registry.register(JsonCollector('10.60.17.231', ['database-node', 'analytics-node', 'config-database-node', 'control-node', 'config-node']))

  start_http_server(9104, registry=registry)

  while True: time.sleep(1)
