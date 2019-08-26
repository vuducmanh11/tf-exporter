import sys
import time
import json, re
import requests
from prometheus_client import start_http_server, Metric, REGISTRY, CollectorRegistry

class JsonCollector(object):
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


if __name__ == '__main__':

  registry = CollectorRegistry()
  registry.register(JsonCollector('10.60.17.231'))
  start_http_server(9104, registry=registry)
  while True: time.sleep(1)
