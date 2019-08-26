import json
UveVirtualNetworkAgent = {
      "acl": {
      "description": "Name of ACL associated with the VN"
      },

      "total_acl_rules": {
      "description": "Count of rules in the ACL associated with the VN"
      } ,

      "in_bandwidth_usage": {
      "description": "Ingress bandwidth usage in bps"
      },

      "out_bandwidth_usage": {
      "description": "Egress bandwidth usage in bps"
      },

      "ingress_flow_count": {
      "description": "Number of ingress flows in this VN"
      },

      "egress_flow_count": {
      "description": "Number of egress flows in this VN"
      },

      "virtualmachine_list": {
      "description": "List of configuration names of VMs part of this VN"
      },

      "interface_list": {
      "description": "List of configuration names of interfaces part of this VN"
      },

      "associated_fip_count": {
      "description": "Total number of floating-IPs part of this VN. This is sum of floating-IPs associated with all VMIs that are part of this VN"
      },

      "udp_sport_bitmap": {
      "description": "Bitmap of UDP source port numbers that packets on this VN have used"
      },

      "udp_dport_bitmap": {
      "description": "Bitmap of UDP destination port numbers that packets on this VN have used"
      },

      "tcp_sport_bitmap": {
      "description": "Bitmap of TCP source port numbers that packets on this VN have used"
      },

      "tcp_dport_bitmap": {
      "description": "Bitmap of TCP destination port numbers that packets on this VN have used"
      },
      
      "vn_stats": {
      "description": "Statistics of VN with respect to other VNs"
      },
      
      "in_stats": {
      "description": "Incoming statistics for this VN from other VN"
      },
      
      "out_stats": {
      "description": "Outgoing statistics from this VN to other VN"
      },
      
      "vrf_stats_list": {
      "description": "Statistics of VRF associated with VN"
      },
      
    }

for js_metric in UveVirtualNetworkAgent:
  print((js_metric, UveVirtualNetworkAgent[js_metric]["description"]))