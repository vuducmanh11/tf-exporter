import sys
import time
import json, re
import requests
from prometheus_client import start_http_server, Metric, REGISTRY, CollectorRegistry
from flatten_json import flatten

class JsonCollector(object):
  def __init__(self, endpoint):
    self._endpoint = 'http://' + endpoint + ':8081/analytics/uves/virtual-network/*?flat'

  def collect(self):

      # get endpoint
      url = self._endpoint
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
        "type": "list",
        "item_list": {
          "in_bytes": 'Ingress byte count from other vn',
          "other_vn": 'Name of virtual other network',
          "out_bytes": 'Egress byte count from other vn',
          "out_tpkts": 'Egress packet count from other vn',
          "in_tpkts": 'Ingress packet count from other vn',
          "vrouter": 'Name of agent sending information'
          }
        },
        
        "in_stats": {
        "description": "Incoming statistics for this VN from other VN",
        "type": "list",
        "item_list": {
          "bytes": 'Byte count incoming VN include this VN',
          "other_vn": 'Name of  virtual network',
          "tpkts": 'Packet count incoming VN include this VN'
          }
        },
        
        "out_stats": {
        "description": "Outgoing statistics from this VN to other VN",
        "type": "list",
        "item_list": {
          "bytes": 'Byte count outgoing VN',
          "other_vn": 'Name of other virtual network',
          "tpkts": 'Packet count outgoing VN'
          }
        },
        
        "vrf_stats_list": {
        "description": "Statistics of VRF associated with VN",
        "type": "gauge"
        },
        
      }

      vrf_stats_list = {
        'offload_packet_counts_gro': 'Off load packet statistics',
        'unknown_unicast_floods': 'Nexthop statistics',
        'nh_packet_counts_discards': 'Nexthop statistics',
        
        'nh_packet_counts_comp_nh_stats_edge_replication_forwards': 'Multicast nexthop statistics fabric composites',
        'nh_packet_counts_comp_nh_stats_source_replication_forwards': 'Multicast nexthop statistics evpn composites',
        'nh_packet_counts_comp_nh_stats_total_multicast_forwards': 'Multicast nexthop statistics l2 multicast composites',
        'nh_packet_counts_comp_nh_stats_local_vm_l3_forwards': 'Nexthop statistics encaps composites',

        'nh_packet_counts_local_vm_l3_forwards': 'Nexthop statistics encaps',
        'nh_packet_counts_local_vm_l2_forwards': 'Nexthop statistics l2 encaps',
        'nh_packet_counts_l3_receives': 'Nexthop statistics',
        'nh_packet_counts_l2_receives': 'Nexthop statistics',
        'nh_packet_counts_resolves': 'Nexthop statistics',
        'nh_packet_counts_ecmp_forwards': 'Nexthop statistics ecmp composites',
        'nh_packet_counts_vrf_translates': 'Nexthop statistics',
        'nh_packet_counts_tunnel_nh_stats_vxlan_encaps': 'Tunnel nexthop statistics',
        'nh_packet_counts_tunnel_nh_stats_mpls_over_udp_encaps': 'Tunnel nexthop statistics',
        'nh_packet_counts_tunnel_nh_stats_udp_encaps': 'Tunnel nexthop statistics',
        'nh_packet_counts_tunnel_nh_stats_mpls_over_gre_encaps': 'Tunnel nexthop statistics',
        # 'nh_packet_counts_tunnel_nh_stats_': 'not define',
        # 'nh_packet_counts_tunnel_nh_stats_': 'not define',
        # 'name': 'not define',
        'arp_packet_counts_from_vm_interface_stats_floods': 'ARP packet statistics of virtual machine interface',
        'arp_packet_counts_from_vm_interface_stats_proxies': 'ARP packet statistics of virtual machine interface',
        'arp_packet_counts_from_vm_interface_stats_stitches': 'ARP packet statistics of virtual machine interface',
        'arp_packet_counts_from_physical_interface_stats_floods': 'ARP packet statistics of physical',
        'arp_packet_counts_from_physical_interface_stats_proxies': 'ARP packet statistics of physical',
        'arp_packet_counts_from_physical_interface_stats_stitches': 'ARP packet statistics of physical',
        'diag_packet_count': 'not define'

      }

      # Add metric follow above description
      # Loop over all to create metric
      for name_metric in UveVirtualNetworkAgent:
        
        # Create vn_stats_* metric
        if (name_metric == 'vn_stats'):
          for metric_item in UveVirtualNetworkAgent[name_metric]["item_list"]:
            metric = Metric(name_metric+'_'+metric_item, UveVirtualNetworkAgent[name_metric]["item_list"][metric_item], 'gauge')
          # metric = Metric(name_metric, UveVirtualNetworkAgent[name_metric]["description"], UveVirtualNetworkAgent[name_metric]["type"])
            for i in range(number_vnet):

            # Define current virtual network 
              current_json_vnet = json_all_vnet[i]['value']
              name_curr_json_vnet = json_all_vnet[i]['name']
        
              if ('UveVirtualNetworkAgent' in current_json_vnet and name_metric in current_json_vnet['UveVirtualNetworkAgent'] ):

                # Set current metric
                current_metric = current_json_vnet['UveVirtualNetworkAgent'][name_metric]


                for k in range(len(current_metric)):
                  # for stat in current_metric[k]:
                  if(type(current_metric[k]) is dict):
                    if ( type(current_metric[k][metric_item]) is str ):
                      metric.add_sample(name_metric+'_'+metric_item, value = 1, labels={
                        "network_name": re.sub(r'[:-]', '_', name_curr_json_vnet),
                        metric_item: current_metric[k][metric_item]
                        })
                    else:
                      metric.add_sample(name_metric+'_'+metric_item, value = current_metric[k][metric_item], labels={
                        "network_name": re.sub(r'[:-]', '_', name_curr_json_vnet),
                        # "value": stat
                        # metric_item: str(current_metric[k][metric_item])
                        })
                  else:
                    z = current_metric[k][0][0]
                    server = current_metric[k][1]
                    if (type(z[metric_item]) is str):
                      metric.add_sample(name_metric+'_'+metric_item, value = 1, labels={
                        "network_name": re.sub(r'[:-]', '_', name_curr_json_vnet),
                        metric_item: str(z[metric_item]),
                        "server": server
                        })
                    else:
                      metric.add_sample(name_metric+'_'+metric_item, value = z[metric_item] , labels={
                        "network_name": re.sub(r'[:-]', '_', name_curr_json_vnet),
                        "server": server
                        })

            yield metric
        
        # Create vrf_stats_list_* metric
        elif (name_metric == 'vrf_stats_list'):
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





        # Create in_stats_* and out_stats_* metric
        elif (name_metric == 'in_stats' or name_metric == 'out_stats'):
          for metric_item in UveVirtualNetworkAgent[name_metric]['item_list']:
            metric = Metric(name_metric+'_'+metric_item, UveVirtualNetworkAgent[name_metric]["item_list"][metric_item], 'gauge')
            for i in range(number_vnet):
            # Define current virtual network 
              current_json_vnet = json_all_vnet[i]['value']
              name_curr_json_vnet = json_all_vnet[i]['name']
        
              if ('UveVirtualNetworkAgent' in current_json_vnet and name_metric in current_json_vnet['UveVirtualNetworkAgent'] ):

                # Set current metric
                current_metric = current_json_vnet['UveVirtualNetworkAgent'][name_metric]

                for k in range(len(current_metric)):
                  # for stat in current_metric[k]:
                  if (type(current_metric[k][metric_item]) is str):
                    metric.add_sample(name_metric+'_'+metric_item, value = 1, labels={
                      "network_name": re.sub(r'[:-]', '_', name_curr_json_vnet),
                      metric_item: current_metric[k][metric_item]
                      })
                  elif (type(current_metric[k][metric_item]) is int or type(current_metric[k][metric_item]) is float):
                    metric.add_sample(name_metric+'_'+metric_item, value = current_metric[k][metric_item], labels={
                      "network_name": re.sub(r'[:-]', '_', name_curr_json_vnet)
                      })
            yield metric

        # Create manual metric
        else:
          metric = Metric(name_metric, UveVirtualNetworkAgent[name_metric]["description"], UveVirtualNetworkAgent[name_metric]["type"])
          # define number_vnet above

          # Loop over virtual network
          for i in range(number_vnet):

            # Define current virtual network 
            current_json_vnet = json_all_vnet[i]['value']
            name_curr_json_vnet = json_all_vnet[i]['name']
        
            if ('UveVirtualNetworkAgent' in current_json_vnet and name_metric in current_json_vnet['UveVirtualNetworkAgent'] ):

              # Set current metric
              current_metric = current_json_vnet['UveVirtualNetworkAgent'][name_metric]



              # If metric is number
              if ( type(current_metric) is int or  type(current_metric) is float ):
                metric.add_sample(name_metric, value = current_metric, labels={"network_name": re.sub(r'[:-]', '_', name_curr_json_vnet)})

              # If metric is string
              elif (type(current_metric) is str ):
                
                metric.add_sample(name_metric, value = 1, labels={"network_name": re.sub(r'[:-]', '_', name_curr_json_vnet), 
                  "value": current_metric})  

              # If metric is list
              elif ( type(current_metric) is list ):
                if (type(current_metric[0]) is not list):
                  for k in range(len(current_metric)):
                    if (current_metric[k].isdigit()):
                      metric.add_sample(name_metric, value = int(current_metric[k]), labels={
                        "network_name": re.sub(r'[:-]', '_', name_curr_json_vnet),
                        # re.sub(r'_list', '', name_metric): current_metric[k],
                        'index': str(k)
                        })
                    else:
                      metric.add_sample(name_metric, value = 1, labels={
                      "network_name": re.sub(r'[:-]', '_', name_curr_json_vnet),
                      re.sub(r'_list', '', name_metric): current_metric[k],
                      'index': str(k)
                      })
                else:
                  print(name_curr_json_vnet)
                  print(current_metric)
                  for k in range(len(current_metric)):
                    for j in range(len(current_metric[k][0])):
                      metric.add_sample(name_metric, value = int(current_metric[k][0][j]), labels={
                        "network_name": re.sub(r'[:-]', '_', name_curr_json_vnet),
                        "vrouter-agent": current_metric[k][1],
                        'index': str(j)
                        })
                  # for k in range(len(current_metric[0])):
                  #   if (current_metric[0][k].isdigit()):
                  #     metric.add_sample(name_metric, value = int(current_metric[0][k]), labels={
                  #       "network_name": re.sub(r'[:-]', '_', name_curr_json_vnet),
                  #       # re.sub(r'_list', '', name_metric): current_metric[k],
                  #       "vrouter-agent": current_metric
                  #       'index': str(k)
                  #       })
                    # else:
                    #   metric.add_sample(name_metric, value = 1, labels={
                    #   "network_name": re.sub(r'[:-]', '_', name_curr_json_vnet),
                    #   re.sub(r'_list', '', name_metric): current_metric[k],
                    #   'index': str(k)
                    #   })
               
          yield metric



if __name__ == '__main__':
  # Usage python file.py endpoint
  
  registry = CollectorRegistry()
  registry.register(JsonCollector('10.60.17.231'))
  start_http_server(9103, registry=registry)

  while True: time.sleep(1)