import sys
import time
import json, re
import requests
from prometheus_client import start_http_server, Metric, REGISTRY, CollectorRegistry

class BgpCollector(object):
  
  def __init__(self, endpoint):
    self._endpoint = 'http://' + endpoint + ':8081/analytics/uves/bgp-peer/*?flat'

  def collect(self):
    bgp_state = {
      "Idle": '0',
      "Active": '1' ,
      "Connect" : '2',
      "OpenSent": '3',
      "OpenConfirm": '4',
      "Established": '5'
      }
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
        local_id = cbgp['BgpPeerInfoData']['local_id']
        state = cbgp['BgpPeerInfoData']['state_info']['state']
        metric.add_sample('bgp_state_info', value= int(bgp_state[state]) + 1, labels={
          'bgp_last_state': cbgp['BgpPeerInfoData']['state_info']['last_state'],
          'bgp_state': state,
          'control_node': snode,
          'peer': dnode,
          'local_id': str(local_id),
          })
    yield metric


    BgpPeerInfoData = {
      'long_lived_graceful_restart_time': {
        'type': 'gauge',
        'description': 'None'
      },
      'peer_type': {
        'type': 'gauge',
        'description': 'None'
      },
      'origin_override': {
        'type': 'gauge',
        'description': 'None'
      },
      'cluster_id': {
        'type': 'gauge',
        'description': 'None'
      },
      'peer_address': {
        'type': 'gauge',
        'description': 'None'
      },
      'as_override': {
        'type': 'gauge',
        'description': 'None'
      },
      'state_info': {
        'type': 'dict_mix',
        'item_dict_mix': {
          'last_state': 'None',
          'state': 'None',
          'last_state_at': 'None'
        }
        # 'description': 'None'
      },
      'graceful_restart_time': {
        'type': 'gauge',
        'description': 'None'
      },
      'local_asn': {
        'type': 'gauge',
        'description': 'None'
      },
      'event_info': {
        'type': 'dict_mix',
        'item_dict_mix': {
          'last_event_at': 'None',
          'last_event': 'None',
        }
        # 'description': 'None'
      },
      'passive': {
        'type': 'gauge',
        'description': 'None'
      },
      'negotiated_families': {
        'type': 'list_str',
        'description': 'None'
      },
      'peer_id': {
        'type': 'gauge',
        'description': 'None'
      },
      'route_origin': {
        'type': 'gauge',
        'description': 'None'
      },
      'peer_asn': {
        'type': 'gauge',
        'description': 'None'
      },
      'families': {
        'type': 'list_str',
        'description': 'None'
      },
      'admin_down': {
        'type': 'gauge',
        'description': 'None'
      },
      'configured_families': {
        'type': 'list_str',
        'description': 'None'
      },
      'peer_port': {
        'type': 'gauge',
        'description': 'None'
      },
      'hold_time': {
        'type': 'gauge',
        'description': 'None'
      },
      'peer_stats_info': {
        'type': 'dict_dict',
        'description': 'None',
        'item_dict_dict':
        {
          'rx_proto_stats/notification': 'None',
          'rx_proto_stats/update': 'None',
          'rx_proto_stats/close': 'None',
          'rx_proto_stats/total': 'None',
          'rx_proto_stats/keepalive': 'None',
          'tx_proto_stats/notification': 'None',
          'tx_proto_stats/update': 'None',
          'tx_proto_stats/close': 'None',
          'tx_proto_stats/total': 'None',
          'tx_proto_stats/keepalive': 'None',
          'rx_update_stats/unreach': 'None',
          'rx_update_stats/total': 'None',
          'rx_update_stats/reach': 'None',
          'rx_update_stats/end_of_rib': 'None',
          'tx_update_stats/unreach': 'None',
          'tx_update_stats/total': 'None',
          'tx_update_stats/reach': 'None',
          'tx_update_stats/end_of_rib': 'None',
          'rx_route_stats/primary_path_count': 'None',
          'rx_route_stats/total_path_count': 'None',
          'rx_error_stats/inet6_error_stats/bad_inet6_xml_token_count': 'None',
          'rx_error_stats/inet6_error_stats/bad_inet6_afi_safi_count': 'None',
          'rx_error_stats/inet6_error_stats/bad_inet6_nexthop_count': 'None',
          'rx_error_stats/inet6_error_stats/bad_inet6_prefix_count': 'None',
        }
      },
      'local_id': {
        'type': 'gauge',
        'description': 'None'
      },
      'router_type': {
        'type': 'gauge',
        'description': 'None'
      },
    }
    for name_metric in BgpPeerInfoData:
      if (BgpPeerInfoData[name_metric]['type'] == 'gauge'):
        metric = Metric('bgp_'+name_metric, '', 'gauge')
        for i in range(len(json_all_bgp)):
          cbgp = json_all_bgp[i]['value']
          conn = json_all_bgp[i]['name'].split(':')
          if ('BgpPeerInfoData' in cbgp and name_metric in cbgp['BgpPeerInfoData']):
            snode = conn[4]
            dnode = conn[9]
            local_id = cbgp['BgpPeerInfoData']['local_id']
            # if ('peer_id' not in cbgp['BgpPeerInfoData']): print(json_all_bgp[i]['name'])
            if (type(cbgp['BgpPeerInfoData'][name_metric]) in [int,float] ):
              metric.add_sample('bgp_'+name_metric, value = cbgp['BgpPeerInfoData'][name_metric], labels={
                'local_id': str(local_id),
                'control_node': snode,
                'peer': dnode,
                })
            elif (type(cbgp['BgpPeerInfoData'][name_metric]) is str):
              metric.add_sample('bgp_'+name_metric, value = 1, labels={
                name_metric: cbgp['BgpPeerInfoData'][name_metric],
                'local_id': str(local_id),
                'control_node': snode,
                'peer': dnode,
                })
        yield metric
      elif (BgpPeerInfoData[name_metric]['type'] == 'dict_mix'):
        for metric_item in BgpPeerInfoData[name_metric]['item_dict_mix']:
          metric = Metric('bgp_'+name_metric + '_' + metric_item, BgpPeerInfoData[name_metric]['item_dict_mix'][metric_item], 'gauge')
          for i in range(len(json_all_bgp)):
            cbgp = json_all_bgp[i]['value']
            conn = json_all_bgp[i]['name'].split(':')
            if ('BgpPeerInfoData' in cbgp and name_metric in cbgp['BgpPeerInfoData']):
              snode = conn[4]
              dnode = conn[9]
              local_id = cbgp['BgpPeerInfoData']['local_id']
              if (type(cbgp['BgpPeerInfoData'][name_metric][metric_item]) in [int,float] ):
                metric.add_sample('bgp_'+name_metric + '_' + metric_item, value = cbgp['BgpPeerInfoData'][name_metric][metric_item], labels={
                  'local_id': str(local_id),
                  'control_node': snode,
                  'peer': dnode,
                  })
              elif (type(cbgp['BgpPeerInfoData'][name_metric][metric_item]) is str):
                metric.add_sample('bgp_'+name_metric + '_' + metric_item, value = 1, labels={
                  metric_item: cbgp['BgpPeerInfoData'][name_metric][metric_item],
                  'local_id': str(local_id),
                  'control_node': snode,
                  'peer': dnode,
                  })
          yield metric
      elif (BgpPeerInfoData[name_metric]['type'] == 'list_str'):
        metric = Metric('bgp_'+name_metric, BgpPeerInfoData[name_metric]['description'], 'gauge')
        for i in range(len(json_all_bgp)):
          cbgp = json_all_bgp[i]['value']
          conn = json_all_bgp[i]['name'].split(':')
          if ('BgpPeerInfoData' in cbgp and name_metric in cbgp['BgpPeerInfoData']):
            snode = conn[4]
            dnode = conn[9]
            local_id = cbgp['BgpPeerInfoData']['local_id']
            for k in range(len(cbgp['BgpPeerInfoData'][name_metric])):
              metric.add_sample('bgp_'+name_metric, value = 1, labels={
                name_metric: cbgp['BgpPeerInfoData'][name_metric][k],
                'local_id': str(local_id),
                'control_node': snode,
                'peer': dnode,
                })
        yield metric
      elif (BgpPeerInfoData[name_metric]['type'] == 'dict_dict'):
        for metric_item in BgpPeerInfoData[name_metric]['item_dict_dict']:
          item = metric_item
          path = metric_item.split('/')
          metric_item = metric_item.replace('/','_')
          metric = Metric('bgp_'+metric_item, BgpPeerInfoData[name_metric]['item_dict_dict'][item], 'gauge')
          for i in range(len(json_all_bgp)):
            cbgp = json_all_bgp[i]['value']
            conn = json_all_bgp[i]['name'].split(':')
            if ('BgpPeerInfoData' in cbgp and name_metric in cbgp['BgpPeerInfoData']):
              snode = conn[4]
              dnode = conn[9]
              
              value = cbgp['BgpPeerInfoData'][name_metric]
              for k in range(len(path)):
                value = value[path[k]]
              metric.add_sample('bgp_'+metric_item, value = value, labels={
                'local_id': str(local_id),
                'control_node': snode,
                'peer': dnode,
                })
          yield metric 




class XmppCollector(object):
  def __init__(self, endpoint):
    self._endpoint = 'http://' + endpoint + ':8081/analytics/uves/xmpp-peer/*?flat'

  def collect(self):
    xmpp_state = {
      "Idle": '0',
      "Active": '1' ,
      "Connect" : '2',
      "OpenSent": '3',
      "OpenConfirm": '4',
      "Established": '5'
      }
    XmppPeerInfoData = {
      'state_info': {
        'type': 'dict_mix',
        'item_dict_mix': {
          'last_state': 'None',
          'state': 'None',
          'last_state_at': 'None'
        }
        # 'description': 'None'
      },
      'peer_stats_info': {
        'type': 'dict_dict',
        'description': 'None',
        'item_dict_dict':
        {
          'rx_proto_stats/notification': 'None',
          'rx_proto_stats/update': 'None',
          'rx_proto_stats/close': 'None',
          'rx_proto_stats/total': 'None',
          'rx_proto_stats/keepalive': 'None',
          'tx_proto_stats/notification': 'None',
          'tx_proto_stats/update': 'None',
          'tx_proto_stats/close': 'None',
          'tx_proto_stats/total': 'None',
          'tx_proto_stats/keepalive': 'None',
          'rx_update_stats/unreach': 'None',
          'rx_update_stats/total': 'None',
          'rx_update_stats/reach': 'None',
          'rx_update_stats/end_of_rib': 'None',
          'tx_update_stats/unreach': 'None',
          'tx_update_stats/total': 'None',
          'tx_update_stats/reach': 'None',
          'tx_update_stats/end_of_rib': 'None',
          'rx_route_stats/primary_path_count': 'None',
          'rx_route_stats/total_path_count': 'None',
          'rx_error_stats/inet6_error_stats/bad_inet6_xml_token_count': 'None',
          'rx_error_stats/inet6_error_stats/bad_inet6_afi_safi_count': 'None',
          'rx_error_stats/inet6_error_stats/bad_inet6_nexthop_count': 'None',
          'rx_error_stats/inet6_error_stats/bad_inet6_prefix_count': 'None',
        }
      },
      'event_info': {
        'type': 'dict_mix',
        'item_dict_mix': {
          'last_event_at': 'None',
          'last_event': 'None',
        }
        # 'description': 'None'
      },

    }
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
          state = cxmpp['XmppPeerInfoData']['state_info']['state']
          metric.add_sample('xmpp_state_info', value = int(xmpp_state[state]) + 1, labels={
            'last_event': cxmpp['XmppPeerInfoData']['event_info']['last_event'],
            'control_node': control_node,
            'compute_node': compute_node,
            'state': cxmpp['XmppPeerInfoData']['state_info']['state'],
            })
    yield metric

    for name_metric in XmppPeerInfoData:
      if(XmppPeerInfoData[name_metric]['type'] == 'dict_dict'):
        for metric_item in XmppPeerInfoData[name_metric]['item_dict_dict']:
          item = metric_item
          path = metric_item.split('/')
          metric_item = metric_item.replace('/','_')
          metric = Metric('xmpp_'+metric_item, XmppPeerInfoData[name_metric]['item_dict_dict'][item], 'gauge')
          for i in range(len(json_all_xmpp)):
            cxmpp = json_all_xmpp[i]['value']
            conn =  json_all_xmpp[i]['name'].split(':')
            control_node = conn[0]
            compute_node = conn[1]
            if ('XmppPeerInfoData' in cxmpp and name_metric in cxmpp['XmppPeerInfoData']):
              
              value = cxmpp['XmppPeerInfoData'][name_metric]
              for k in range(len(path)):
                value = value[path[k]]
              metric.add_sample('xmpp_'+metric_item, value = value, labels={
                'control_node': control_node,
                'compute_node': compute_node,
                })
          yield metric 

      elif(XmppPeerInfoData[name_metric]['type'] == 'dict_mix'):
        for metric_item in XmppPeerInfoData[name_metric]['item_dict_mix']:
          metric = Metric('xmpp_'+name_metric + '_' + metric_item, XmppPeerInfoData[name_metric]['item_dict_mix'][metric_item], 'gauge')
          for i in range(len(json_all_xmpp)):
            cxmpp = json_all_xmpp[i]['value']
            conn =  json_all_xmpp[i]['name'].split(':')
            control_node = conn[0]
            compute_node = conn[1]
            if ('XmppPeerInfoData' in cxmpp and name_metric in cxmpp['XmppPeerInfoData']):
              if (type(cxmpp['XmppPeerInfoData'][name_metric][metric_item]) in [int,float] ):
                metric.add_sample('xmpp_'+name_metric + '_' + metric_item, value = cxmpp['XmppPeerInfoData'][name_metric][metric_item], labels={
                  'control_node': control_node,
                  'compute_node': compute_node,
                  })
              elif (type(cxmpp['XmppPeerInfoData'][name_metric][metric_item]) is str):
                metric.add_sample('xmpp_'+name_metric + '_' + metric_item, value = 1, labels={
                  metric_item: cxmpp['XmppPeerInfoData'][name_metric][metric_item],
                  'control_node': control_node,
                  'compute_node': compute_node,
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
          metric.add_sample('contrail_status', value = 1 if current_metric[k]['process_state'] == 'PROCESS_STATE_RUNNING' else 0, labels = {
              'process_name': current_metric[k]['process_name'],
              'process_state': current_metric[k]['process_state'],
              'last_start_time': current_metric[k]['last_start_time'],
              'node': re.sub('.local','',json_all_node[i]['name']),
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
