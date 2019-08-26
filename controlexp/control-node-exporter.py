import sys
import time
import json, re
import requests
from prometheus_client import start_http_server, Metric, REGISTRY, CollectorRegistry
from flatten_json import flatten

class JsonCollector(object):
  def __init__(self, endpoint):
    self._endpoint = 'http://' + endpoint + ':8081/analytics/uves/control-node/*?flat'

  def collect(self):

    # get metric about control nodes
    url = self._endpoint

    # Fetch the JSON
    response = json.loads(requests.get(url).content.decode('UTF-8'))
    json_all_cnode = response['value']
    number_cnode = len(json_all_cnode)
    
    # Add metric system_mem_usage_used
    NodeStatus = {
    'process_info': {
      'type': 'list',
      'item_list': {
        'process_name': {
          'description': '',
          'type': 'string'
        },
        'process_state': {
          'description': '',
          'type': 'string'
        },
        'last_stop_time': {
          'description': '',
          'type': 'string'
        },
        'start_count': {
          'description': '',
          'type': 'int'
        },
        # 'core_file_list': {
        #   'description': '',
        #   'type': 'string'
        # },
        'last_start_time': {
          'description': '',
          'type': 'string'
        },
        'stop_count': {
          'description': '',
          'type': 'int'
        },
        'last_exit_time': {
          'description': '',
          'type': 'string'
        },
        'exit_count': {
          'description': '',
          'type': 'int'
        },
      }
    }
    }

    # for name_metric in NodeStatus:
    #   if NodeStatus[name_metric]['type'] == "string":
    #     print 1
    #   elif NodeStatus[name_metric]['type'] == "list":
    #     for name_item_list in NodeStatus[name_metric]['item_list']:
    #       if (NodeStatus[name_metric]['item_list'][name_item_list]['type'] == 'string'):
    #         metric = Metric(name_metric + '_'+name_item_list, NodeStatus[name_metric][name_item_list]['description'], 'gauge')
    #         for i in range(number_cnode):
    #           current_json_cnode = json_all_cnode[i]['value']
    #           metric.add_sample(name_metric + '_'+name_item_list, value = current_json_cnode['NodeStatus'][name_metric])
    # for name_metric in NodeStatus['process_info']:
    metric = Metric('contrail_status', '', 'gauge')
    for i in range(number_cnode):
      current_json_cnode = json_all_cnode[i]['value']
      current_metric = current_json_cnode['NodeStatus']['process_info']
      for k in range(len(current_metric)):
        metric.add_sample('contrail_status', value = 1, labels = {
            'process_name': current_metric[k]['process_name'],
            'process_state': current_metric[k]['process_state'],
            'last_start_time': current_metric[k]['last_start_time'],
            'control_node': json_all_cnode[i]['name']
          })
    yield metric

    metric = Metric('control_node_avl', 'List of control node available', 'gauge')
    for i in range(number_cnode):
      metric.add_sample('control_node_avl', value = 1, labels = {
        'control_name': json_all_cnode[i]['name']
        })
    yield metric


if __name__ == '__main__':
  # Usage python file.py port endpoint
  registry = CollectorRegistry()
  registry.register(JsonCollector('10.60.17.231'))
  start_http_server(9101, registry=registry)

  while True: time.sleep(1)
