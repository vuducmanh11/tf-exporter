import sys, time, json, re
import requests
from prometheus_client import start_http_server, Metric, REGISTRY, CollectorRegistry

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

    # Add metric follow above description
    # Loop over all to create metric
    for name_metric in UveVirtualNetworkAgent:
      # Create object Metric
      metric = Metric(name_metric, UveVirtualNetworkAgent[name_metric]["description"], UveVirtualNetworkAgent[name_metric]["type"])
      # define number_vnet above

      # Loop over virtual network
      for i in range(number_vnet):

        # Define current virtual network 
        current_json_vnet = json_all_vnet[i]['value']
        name_curr_json_vnet = json_all_vnet[i]['name']
        # if ('UveVirtualNetworkAgent' in current_json_vnet and name_metric in current_json_vnet['UveVirtualNetworkAgent'] and (type(current_json_vnet['UveVirtualNetworkAgent'][name_metric]) is int or  type(current_json_vnet['UveVirtualNetworkAgent'][name_metric]) is float) ) :
        #   metric.add_sample(name_metric, value = current_json_vnet['UveVirtualNetworkAgent'][name_metric], labels={"network_name": re.sub(r'[:-]', '_', name_curr_json_vnet)})

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
          elif ( type(current_metric) is list and type(current_metric[0]) is str):
            for k in range(len(current_metric)):
              metric.add_sample(name_metric, value = 1, labels={
                "network_name": re.sub(r'[:-]', '_', name_curr_json_vnet),
                name_metric+str('_')+str(k): current_metric[k]
                })

      yield metric

if __name__ == '__main__':

  registry = CollectorRegistry()
  registry.register(JsonCollector('10.60.17.231'))
  start_http_server(9109, registry=registry)
  while True: time.sleep(1)
