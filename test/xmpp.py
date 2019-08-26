import sys
import time
import json, re
import requests
from prometheus_client import start_http_server, Metric, REGISTRY, CollectorRegistry

class JsonCollector(object):
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

    # metric = Metric('xmpp_state_info', '', 'gauge')
    # for i in range(len(json_all_xmpp)):
    #   cxmpp = json_all_xmpp[i]['value']
    #   if ('XmppPeerInfoData' in cxmpp and 'state_info' in cxmpp['XmppPeerInfoData']):
    #     metric.add_sample('xmpp_state_info', value = 1, labels={
    #       'last_state': cxmpp['XmppPeerInfoData']['state_info']['last_state'],
    #       'state': cxmpp['XmppPeerInfoData']['state_info']['state'],
    #       'conn': json_all_xmpp[i]['name']
    #       })
    # yield metric

if __name__ == '__main__':

  registry = CollectorRegistry()
  registry.register(JsonCollector('10.60.17.231'))
  start_http_server(9104, registry=registry)
  while True: time.sleep(1)
