import sys
import time
import json, re
import requests
from prometheus_client import start_http_server, Metric, REGISTRY, CollectorRegistry

class BgpCollector(object):
  def __init__(self, endpoint):
    self._endpoint = 'http://' + endpoint + ':8081/analytics/uves/bgp-peer/*?flat'

  def collect(self):

    url = self._endpoint
    response = json.loads(requests.get(url).content.decode('UTF-8'))
    json_all_bgp = response['value']
    metric = Metric('bgp_state_info', '', 'gauge')
    for i in range(len(json_all_bgp)):
      cbgp = json_all_bgp[i]['value']
      conn = json_all_bgp[i]['name'].split(':')
      snode = conn[4]
      dnode = conn[9]
      if ('BgpPeerInfoData' in cbgp and 'state_info' in cbgp['BgpPeerInfoData']):
        metric.add_sample('bgp_state_info', value=1, labels={
          'bgp_last_state': cbgp['BgpPeerInfoData']['state_info']['last_state'],
          'bgp_state': cbgp['BgpPeerInfoData']['state_info']['state'],
          'control_node': snode,
          'peer': dnode

          })
    yield metric
class XmppCollector(object):
  def __init__(self, endpoint):
    self._endpoint = 'http://' + endpoint + ':8081/analytics/uves/xmpp-peer/*?flat'

  def collect(self):

    url = self._endpoint
    response = json.loads(requests.get(url).content.decode('UTF-8'))
    json_all_xmpp = response['value']

    metric = Metric('xmpp_state_info', '', 'gauge')
    for i in range(len(json_all_xmpp)):
      cxmpp = json_all_xmpp[i]['value']
      conn =  json_all_xmpp[i]['name'].split(':')
      control_node = conn[0]
      compute_node = conn[1]
      if ('XmppPeerInfoData' in cxmpp and 'event_info' in cxmpp['XmppPeerInfoData']):
        if ('state_info' not in cxmpp['XmppPeerInfoData']):
          metric.add_sample('xmpp_state_info', value = 0, labels={
            'last_event': cxmpp['XmppPeerInfoData']['event_info']['last_event'],
            'control_node': control_node,
            'compute_node': compute_node,
            'state': 'null'
            })
        else:
          metric.add_sample('xmpp_state_info', value = 1, labels={
            'last_event': cxmpp['XmppPeerInfoData']['event_info']['last_event'],
            'control_node': control_node,
            'compute_node': compute_node,
            'state': cxmpp['XmppPeerInfoData']['state_info']['state'],  
            })
    yield metric

class ClusterCollector(object):
  def __init__(self, endpoint, uve_type):
    self._node = uve_type
    self._endpoint = []
    for i in range(len(uve_type)):
      self._endpoint.append('http://' + endpoint + ':8081/analytics/uves/' + uve_type[i] +'/*?flat')

  def collect(self):

    # get metric about control nodes
    urls = self._endpoint

    metric = Metric('contrail_status', '', 'gauge')

    # Fetch the JSON
    for j in range(len(urls)):

      response = json.loads(requests.get(urls[j]).content.decode('UTF-8'))
      json_all_node = response['value']
      number_node = len(json_all_node)
      
      # Add metric system_mem_usage_used
      
      # metric = Metric('contrail_status', '', 'gauge')
      for i in range(number_node):
        current_json_node = json_all_node[i]['value']
        current_metric = current_json_node['NodeStatus']['process_info']
        for k in range(len(current_metric)):
          metric.add_sample('contrail_status', value = 0 if current_metric[k]['process_state'] == 'PROCESS_STATE_EXITED' else 1, labels = {
              'process_name': current_metric[k]['process_name'],
              'process_state': current_metric[k]['process_state'],
              'last_start_time': current_metric[k]['last_start_time'],
              'node': json_all_node[i]['name'],
              'node_type': re.sub(r'[:-]', '_', self._node[j])
            })
    yield metric
    # Metric
    for j in range(len(urls)):

      response = json.loads(requests.get(urls[j]).content.decode('UTF-8'))
      json_all_node = response['value']
      number_node = len(json_all_node)
      metric = Metric(re.sub(r'[:-]', '_', self._node[j]), 'List of node available', 'gauge')
      for k in range(number_node):
        metric.add_sample(re.sub(r'[:-]', '_', self._node[j]), value = 1, labels = {
          'config_host': json_all_node[k]['name']
          })
      yield metric
if __name__ == '__main__':

  registry = CollectorRegistry()
  registry.register(XmppCollector('10.60.17.231'))
  registry.register(BgpCollector('10.60.17.231'))
  registry.register(ClusterCollector('10.60.17.231',['database-node', 'analytics-node', 'config-database-node', 'control-node', 'config-node']))
  start_http_server(9104, registry=registry)
  while True: time.sleep(1)
