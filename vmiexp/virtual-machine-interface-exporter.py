import sys, time, json, re
import requests
from prometheus_client import start_http_server, Metric, REGISTRY, CollectorRegistry

class JsonCollector(object):
  def __init__(self, endpoint):
    self._endpoint = 'http://' + endpoint + ':8081/analytics/uves/virtual-machine-interface/*?flat'

  def collect(self):
    url = self._endpoint
    response = json.loads(requests.get(url).content.decode('UTF-8'))
    json_all_vmi = response['value']
    num_vmi = len(json_all_vmi)

    # Description
    UveVMInterfaceAgent = {
      'ip6_active': {
        'type': 'gauge',
        'description': ''
      },
      'port_mirror_enabled': {
        'type': 'gauge',
        'description': 'shows whether interface port mirror is enabled or not'
      },
      'vm_uuid': {
        'type': 'gauge',
        'description': ''
      },
      'ip6_address': {
        'type': 'gauge',
        'description': 'Primary IP version 6 address of VMI'
      },
      'tx_vlan': {
        'type': 'gauge',
        'description': 'Transmit VLAN tag for packets over this VMI'
      },
      'gateway': {
        'type': 'gauge',
        'description': 'Ipv4 address of gateway. It is picked from the subnet of primary IP address of VMI'
      },
      'uuid': {
        'type': 'gauge',
        'description': 'UUID of VMI'
      },
      'vhostuser_mode': {
        'type': 'gauge',
        'description': 'Vhostuser mode'
      },
      'ip4_active': {
        'type': 'gauge',
        'description': ''
      },
      'mac_address': {
        'type': 'gauge',
        'description': ''
      },
      'l2_active': {
        'type': 'gauge',
        'description': ''
      },
      'fixed_ip4_list': {
        'type': 'list',
        'description': 'List of IPv4 addresses assigned to VMI'
      },
      'vm_name': {
        'type': 'gauge',
        'description': ''
      },
      'is_health_check_active': {
        'type': 'gauge',
        'description': 'Contains true if the health check status of VMI is active and false otherwise'
      },
      'admin_state': {
        'type': 'gauge',
        'description': 'Contains true if the VMI is administratively UP and false otherwise'
      },
      'active': {
        'type': 'gauge',
        'description': ''
      },
      'ip_address': {
        'type': 'gauge',
        'description': ''
      },
      'rx_vlan': {
        'type': 'gauge',
        'description': 'Recieve VLAN tag for packets over this VMI'
      },
      'vn_uuid': {
        'type': 'gauge',
        'description': 'UUID of Virtual machine to which the VMI belongs'
      },
      'virtual_network': {
        'type': 'gauge',
        'description': ''
      },
    }
    for name_metric in UveVMInterfaceAgent:
      if (UveVMInterfaceAgent[name_metric]['type'] == 'gauge'):
        metric = Metric(name_metric, UveVMInterfaceAgent[name_metric]['description'], 'gauge')
        for i in range(num_vmi):
          current_json_vmi = json_all_vmi[i]['value']
          name_current_vmi = json_all_vmi[i]['name']
          if ('UveVMInterfaceAgent' in current_json_vmi and name_metric in current_json_vmi['UveVMInterfaceAgent']):
            current_metric = current_json_vmi['UveVMInterfaceAgent'][name_metric]
            if (type(current_metric) is int or  type(current_metric) is float):
              metric.add_sample(name_metric, value = current_metric, labels={
                "virtual_machine_interface": name_current_vmi
                })
            elif (current_metric == 'true'):
              metric.add_sample(name_metric, value = 1, labels={
                "virtual_machine_interface": name_current_vmi
                })
            elif (current_metric == 'false'):
              metric.add_sample(name_metric, value = 0, labels={
                "virtual_machine_interface": name_current_vmi
                })
            elif (type(current_metric) is str ):
              metric.add_sample(name_metric, value = 1, labels={
                "virtual_machine_interface": name_current_vmi,
                name_metric: current_metric
                })
        yield metric

      elif(UveVMInterfaceAgent[name_metric]['type'] == 'list'):
        metric = Metric(name_metric, UveVMInterfaceAgent[name_metric]['description'], 'gauge')
        for i in range(num_vmi):
          current_json_vmi = json_all_vmi[i]['value']
          name_current_vmi = json_all_vmi[i]['name']
          if ('UveVMInterfaceAgent' in current_json_vmi and name_metric in current_json_vmi['UveVMInterfaceAgent'] and type(current_json_vmi['UveVMInterfaceAgent'][name_metric]) is list):
            current_metric = current_json_vmi['UveVMInterfaceAgent'][name_metric]
            for k in range(len(current_json_vmi['UveVMInterfaceAgent'][name_metric])):
              if (type(current_metric[k]) is str):
                metric.add_sample(name_metric, value = 1, labels={
                  "virtual_machine_interface": name_current_vmi,
                  name_metric: current_metric[k]
                  })
        yield metric


    VMIStats = {
      'raw_if_stats': {
        'type': 'dict_int',
        'item_dict': {
          "out_bytes": 'Statistics of VMI. Contains aggregate statistics. Count of outgoing bytes',
          'in_bytes': 'Statistics of VMI. Contains aggregate statistics. Count of incoming bytes',
          'in_pkts': 'Statistics of VMI. Contains aggregate statistics. Count of incoming packets',
          'out_pkts': 'Statistics of VMI. Contains aggregate statistics. Count of outgoing packets'
        }
      },
      'in_bw_usage': {
        'type': 'gauge',
        'description': 'Ingress direction bandwidth in bits per second',
      },
      'out_bw_usage': {
        'type': 'gauge',
        'description': 'Egress direction bandwidth in bits per second',
      },
      'raw_drop_stats': {
        'type': 'dict_int',
        'item_dict': {
          'ds_rewrite_fail': 'not define',
          'ds_mcast_df_bit': 'not define',
          'ds_flow_no_memory': 'not define',
          'ds_push': 'not define',
          'ds_invalid_if': 'not define',
          'ds_pull': 'not define',
          'ds_no_fmd': 'not define',
          'ds_invalid_arp': 'not define',
          'ds_trap_no_if': 'not define',
          'ds_vlan_fwd_tx': 'not define',
          'ds_drop_pkts': 'not define',
          'ds_cksum_err': 'not define',
          'ds_invalid_source': 'not define',
          'ds_flow_action_invalid': 'not define',
          'ds_invalid_packet': 'not define',
          'ds_flow_invalid_protocol': 'not define',
          'ds_invalid_vnid': 'not define',
          'ds_flow_table_full': 'not define',
          'ds_invalid_label': 'not define',
          'ds_frag_err': 'not define',
          'ds_vlan_fwd_enq': 'not define',
          'ds_drop_new_flow': 'not define',
          'ds_duplicated': 'not define',
          'ds_no_memory': 'not define',
          'ds_misc': 'not define',
          'ds_trap_original': 'not define',
          'ds_interface_rx_discard': 'not define',
          'ds_flow_unusable': 'not define',
          'ds_mcast_clone_fail': 'not define',
          'ds_invalid_protocol': 'not define',
          'ds_interface_tx_discard': 'not define',
          'ds_flow_action_drop': 'not define',
          'ds_nowhere_to_go': 'not define',
          'ds_l2_no_route': 'not define',
          'ds_flow_evict': 'not define',
          'ds_invalid_mcast_source': 'not define',
          'ds_discard': 'not define',
          'ds_flow_queue_limit_exceeded': 'not define',
          'ds_flow_nat_no_rflow': 'not define',
          'ds_invalid_nh': 'not define',
          'ds_head_alloc_fail': 'not define',
          'ds_interface_drop': 'not define',
          'ds_pcow_fail': 'not define',
          'ds_ttl_exceeded': 'not define',
          'ds_fragment_queue_fail': 'not define',
        }
      },
      'policy_rules': {
        'type': 'list_str',
        'description': 'not define',
      },
      'flow_rate': {
        'type': 'dict_int',
        'item_dict': {
          'active_flows': 'not define',
          'max_flow_deletes_per_second': 'not define',
          'added_flows': 'not define',
          'deleted_flows': 'not define',
          'min_flow_adds_per_second': 'not define',
          'min_flow_deletes_per_second': 'not define',
          'max_flow_adds_per_second': 'not define',
          'hold_flows': 'not define',
        }
      },
      'port_bucket_bmap': {
        'type': 'dict_list_int',
        'item_dict': {
          'udp_sport_bitmap': 'Bitmap of UDP source port numbers that packets on this VMI have used.',
          'tcp_dport_bitmap': 'Bitmap of TCP destination port numbers that packets on this VMI have used.',
          'tcp_sport_bitmap': 'Bitmap of TCP source port numbers that packets on this VMI have used.',
          'udp_dport_bitmap': 'Bitmap of UDP destination port numbers that packets on this VMI have used.',

        }
      }
    }
    for name_metric in VMIStats:
      if (VMIStats[name_metric]['type'] == 'dict_int'):
        for name_metric_item in VMIStats[name_metric]['item_dict']:
          metric = Metric(name_metric +'_'+ name_metric_item, VMIStats[name_metric]['item_dict'][name_metric_item], 'gauge')
          for i in range(num_vmi):
            current_json_vmi = json_all_vmi[i]['value']
            name_current_vmi = json_all_vmi[i]['name']
            if ('VMIStats' in current_json_vmi and name_metric in current_json_vmi['VMIStats']):
              metric.add_sample(name_metric +'_'+ name_metric_item, value = current_json_vmi['VMIStats'][name_metric][name_metric_item], labels={
                  "virtual_machine_interface": name_current_vmi,
                })
          yield metric
      elif (VMIStats[name_metric]['type'] == 'gauge'):
        metric = Metric(name_metric, VMIStats[name_metric]['description'], 'gauge')
        for i in range(num_vmi):
          current_json_vmi = json_all_vmi[i]['value']
          name_current_vmi = json_all_vmi[i]['name']
          if ('VMIStats' in current_json_vmi and name_metric in current_json_vmi['VMIStats']):
            metric.add_sample(name_metric, value = current_json_vmi['VMIStats'][name_metric], labels={
              "virtual_machine_interface": name_current_vmi
              })
        yield metric
      elif (VMIStats[name_metric]['type'] == 'list_str'):
        metric = Metric(name_metric, VMIStats[name_metric]['description'], 'gauge')
        for i in range(num_vmi):
          current_json_vmi = json_all_vmi[i]['value']
          name_current_vmi = json_all_vmi[i]['name']
          if ('VMIStats' in current_json_vmi and name_metric in current_json_vmi['VMIStats']):
            current_metric = current_json_vmi['VMIStats'][name_metric]
            for k in range(len(current_metric)):
              metric.add_sample(name_metric, value = 1, labels={
                "virtual_machine_interface": name_current_vmi,
                name_metric: current_metric[k]
                })
        yield metric
      elif (VMIStats[name_metric]['type']) == 'dict_list_int':
        for name_metric_item in VMIStats[name_metric]['item_dict']:
          metric = Metric(name_metric + '_' + name_metric_item, VMIStats[name_metric]['item_dict'][name_metric_item], 'gauge')
          for i in range(num_vmi):
            current_json_vmi = json_all_vmi[i]['value']
            name_current_vmi = json_all_vmi[i]['name']
            if( 'VMIStats' in current_json_vmi and name_metric in current_json_vmi['VMIStats']):
              current_metric = current_json_vmi['VMIStats'][name_metric][name_metric_item]
              for k in range(len(current_metric)):
                metric.add_sample(name_metric + '_' + name_metric_item, value = current_metric[k], labels={
                  "virtual_machine_interface": name_current_vmi,
                  })
          yield metric

if __name__ == '__main__':
  registry = CollectorRegistry()
  registry.register(JsonCollector('10.60.17.231'))
  start_http_server(9105, registry=registry)

  while True: time.sleep(1)








