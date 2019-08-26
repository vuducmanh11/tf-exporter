import sys, time, json, re
import requests
from prometheus_client import start_http_server, Metric, REGISTRY, CollectorRegistry
from flatten_json import flatten

class JsonCollector(object):
  def __init__(self, endpoint):
    self._endpoint = 'http://' + endpoint + ':8081/analytics/uves/virtual-network/*?flat'
  
  def collect(self):

    # get endpoint
    url = self._endpoint
    global response, x
    # Fetch the JSON 
    response = json.loads(requests.get(url).content.decode('UTF-8'))
    json_all_vnet = response['value']
    number_vnet = len(json_all_vnet)

    # Add description
    UveVirtualNetworkAgent = {
      "acl": {
      "description": "Name of ACL associated with the VN",
      "type": "gauge"
      },

      "total_acl_rules": {
      "description": "Count of rules in the ACL associated with the VN",
      "type": "gauge"
      } ,

      "in_bandwidth_usage": {
      "description": "Ingress bandwidth usage in bps",
      "type": "gauge"
      },

      "out_bandwidth_usage": {
      "description": "Egress bandwidth usage in bps",
      "type": "gauge"
      },

      "ingress_flow_count": {
      "description": "Number of ingress flows in this VN",
      "type": "gauge"
      },

      "egress_flow_count": {
      "description": "Number of egress flows in this VN",
      "type": "gauge"
      },

      "virtualmachine_list": {
      "description": "List of configuration names of VMs part of this VN",
      "type": "gauge"
      },

      "interface_list": {
      "description": "List of configuration names of interfaces part of this VN",
      "type": "gauge"
      },

      "associated_fip_count": {
      "description": "Total number of floating-IPs part of this VN. This is sum of floating-IPs associated with all VMIs that are part of this VN",
      "type": "gauge"
      },

      "udp_sport_bitmap": {
      "description": "Bitmap of UDP source port numbers that packets on this VN have used",
      "type": "gauge"
      },

      "udp_dport_bitmap": {
      "description": "Bitmap of UDP destination port numbers that packets on this VN have used",
      "type": "gauge"
      },

      "tcp_sport_bitmap": {
      "description": "Bitmap of TCP source port numbers that packets on this VN have used",
      "type": "gauge"
      },

      "tcp_dport_bitmap": {
      "description": "Bitmap of TCP destination port numbers that packets on this VN have used",
      "type": "gauge"
      },
      
      "vn_stats": {
      "description": "Statistics of VN with respect to other VNs",
      "type": "gauge"
      },
      
      "in_stats": {
      "description": "Incoming statistics for this VN from other VN",
      "type": "gauge"
      },
      
      "out_stats": {
      "description": "Outgoing statistics from this VN to other VN",
      "type": "gauge"
      },
      
      "vrf_stats_list": {
      "description": "Statistics of VRF associated with VN",
      "type": "gauge"
      },
      
    }
    vrf_stats_list = {
    'offload_packet_counts_gro': 'not define',
    'unknown_unicast_floods': 'not define',
    'nh_packet_counts_discards': 'not define',
    'nh_packet_counts_local_vm_l3_forwards': 'not define',
    'nh_packet_counts_comp_nh_stats_edge_replication_forwards': 'not define',
    'nh_packet_counts_comp_nh_stats_source_replication_forwards': 'not define',
    'nh_packet_counts_comp_nh_stats_total_multicast_forwards': 'not define',
    'nh_packet_counts_comp_nh_stats_local_vm_l3_forwards': 'not define',
    'nh_packet_counts_local_vm_l2_forwards': 'not define',
    'nh_packet_counts_l3_receives': 'not define',
    'nh_packet_counts_l2_receives': 'not define',
    'nh_packet_counts_resolves': 'not define',
    'nh_packet_counts_ecmp_forwards': 'not define',
    'nh_packet_counts_vrf_translates': 'not define',
    'nh_packet_counts_tunnel_nh_stats_vxlan_encaps': 'not define',
    'nh_packet_counts_tunnel_nh_stats_mpls_over_udp_encaps': 'not define',
    'nh_packet_counts_tunnel_nh_stats_udp_encaps': 'not define',
    'nh_packet_counts_tunnel_nh_stats_mpls_over_gre_encaps': 'not define',
    # 'nh_packet_counts_tunnel_nh_stats_': 'not define',
    # 'nh_packet_counts_tunnel_nh_stats_': 'not define',
    'name': 'not define',
    'arp_packet_counts_from_vm_interface_stats_floods': 'not define',
    'arp_packet_counts_from_vm_interface_stats_proxies': 'not define',
    'arp_packet_counts_from_vm_interface_stats_stitches': 'not define',
    'arp_packet_counts_from_physical_interface_stats_floods': 'not define',
    'arp_packet_counts_from_physical_interface_stats_proxies': 'not define',
    'arp_packet_counts_from_physical_interface_stats_stitches': 'not define',
    'diag_packet_count': 'not define'

    }

    # Add metric follow above description
    # Loop over all to create metric
    for name_metric in UveVirtualNetworkAgent:
      # Create object Metric
      # metric = Metric(name_metric, UveVirtualNetworkAgent[name_metric]["description"], UveVirtualNetworkAgent[name_metric]["type"])
      # define number_vnet above
      if (name_metric == 'vrf_stats_list'):
        for metric_item in vrf_stats_list:
          metric = Metric('vrf_stats_list_'+metric_item, vrf_stats_list[metric_item], UveVirtualNetworkAgent[name_metric]["type"])
          for i in range(number_vnet):
            current_json_vnet = json_all_vnet[i]['value']
            name_curr_json_vnet = json_all_vnet[i]['name']
            if ('UveVirtualNetworkAgent' in current_json_vnet and name_metric in current_json_vnet['UveVirtualNetworkAgent'] ):
              current_metric = current_json_vnet['UveVirtualNetworkAgent'][name_metric]
              metric_list = flatten(current_metric[0])
              if (type(metric_list[metric_item]) is int or type(metric_list[metric_item]) is float):
                metric.add_sample('vrf_stats_list_'+metric_item, value = metric_list[metric_item], labels={
                  'name': metric_item,
                  'network_name': re.sub(r'[:-]', '_', name_curr_json_vnet)
                  })
          yield metric



      # Loop over virtual network
      # for i in range(number_vnet):

      #   # Define current virtual network 
      #   current_json_vnet = json_all_vnet[i]['value']
      #   name_curr_json_vnet = json_all_vnet[i]['name']
      #   print(name_curr_json_vnet)
      #   # if ('UveVirtualNetworkAgent' in current_json_vnet and name_metric in current_json_vnet['UveVirtualNetworkAgent'] and (type(current_json_vnet['UveVirtualNetworkAgent'][name_metric]) is int or  type(current_json_vnet['UveVirtualNetworkAgent'][name_metric]) is float) ) :
      #   #   metric.add_sample(name_metric, value = current_json_vnet['UveVirtualNetworkAgent'][name_metric], labels={"network_name": re.sub(r'[:-]', '_', name_curr_json_vnet)})

      #   if ('UveVirtualNetworkAgent' in current_json_vnet and name_metric in current_json_vnet['UveVirtualNetworkAgent'] ):

      #     current_metric = current_json_vnet['UveVirtualNetworkAgent'][name_metric]
      #     # If metric is list
      #     # if (name_metric == "virtualmachine_list"):
      #     # print(current_metric)
      #     if (name_metric == 'vrf_stats_list'):
      #       metric_list = flatten(current_metric[0])
      #       for metric_item in vrf_stats_list:
      #         metric = Metric('vrf_stats_list_'+metric_item, vrf_stats_list[metric_item], UveVirtualNetworkAgent[name_metric]["type"])
      #         if (type(metric_list[metric_item]) is int or type(metric_list[metric_item]) is float):
      #           metric.add_sample(name_metric, value = metric_list[metric_item], labels={
      #             'name': metric_item,
      #             'network_name': re.sub(r'[:-]', '_', name_curr_json_vnet)
      #             })
      #         #   print(metric_list[metric_item])
      #         # print(type(metric_list[metric_item]))
      #         yield metric
      # # yield metric

if __name__ == '__main__':

  registry = CollectorRegistry()
  registry.register(JsonCollector('10.60.17.231'))
  start_http_server(9001, registry=registry)
  while True: time.sleep(1)
