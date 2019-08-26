import sys
import time
import json
import requests
from prometheus_client import start_http_server, Metric, REGISTRY, CollectorRegistry

class JsonCollector(object):
  def __init__(self, endpoint):
    self._endpoint = 'http://' + endpoint + ':8081/analytics/uves/virtual-machine/*?flat'

  def collect(self):

    # get metric about control nodes

    url = self._endpoint

    # Fetch the JSON
    response = json.loads(requests.get(url).content.decode('UTF-8'))
    
    json_all_vm = response['value']
    number_vm = len(json_all_vm)

    # Description for metrics
    vm_metric = {
    "VirtualMachineStats": {
      "cpu_stats": {
        "virt_memory": {
          "description": "Virtual Memory of VM in kb",
          "type": "gauge"
        },
        "vm_memory_quota": {
          "description": "Total memory of VM in bytes",
          "type": "gauge"
        },
        "peak_virt_memory": {
          "description": "Peak virtual memory of VM in kb",
          "type": "gauge"
        },
        "rss": {
          "description": "Resident set size of VM in bytes",
          "type": "gauge"
        },
        "disk_allocated_bytes": {
          "description": "Allocated disk storage for VM in bytes",
          "type": "gauge"
        },
        "disk_used_bytes": {
          "description": "",
          "type": "gauge"
        },
      }
    },
    "UveVirtualMachineAgent": {
      "vm_state": {
        "description": "State of VM",
        "type": "gauge"
      },
      "vm_cpu_count": {
        "description": "VCPU count specified while launching VM",
        "type": "gauge"
      },
      "vrouter": {
        "description": "Name of the vrouter-agent which hosts current VM",
        "type": "gauge"
      },
      "interface_list": {
        "description": "List of virtual machine interface associated with VM",
        "type": "gauge"
      },
      "udp_sport_bitmap": {
        "description": "Bitmap of UDP source port number that packets on this VM have used" ,
        "type": "gauge"
      },
      "udp_dport_bitmap": {
        "description": "Bitmap of UDP destination port number that packets on this VM have used",
        "type": "gauge"
      },
      "tcp_sport_bitmap": {
        "description": "Bitmap of TCP source port numbers that packets on this VM have used",
        "type": "gauge"
      },
      "tcp_dport_bitmap": {
        "description": "Bitmap of TCP destination port numbers that packets on this VM have used",
        "type": "gauge"
      }
    }
    }
    
    num_vm = len(response['value'])


    for name_metric in vm_metric["VirtualMachineStats"]['cpu_stats'] :
      metric = Metric(name_metric, vm_metric["VirtualMachineStats"]['cpu_stats'][name_metric]["description"], vm_metric["VirtualMachineStats"]['cpu_stats'][name_metric]["type"])

      # Loop over VM
      for i in range(number_vm):
        current_json_vm = json_all_vm[i]['value']
        name_current_vm = json_all_vm[i]['name']

        if('VirtualMachineStats' in current_json_vm and name_metric in current_json_vm['VirtualMachineStats']['cpu_stats'][0]):

          

    # Add metric cpu_stats_virt_memory
    metric = Metric('cpu_stats_virt_memory', 'virt memory used by vm', 'gauge')
    
    for k in range(num_vm):
      if ('VirtualMachineStats' in response['value'][k]['value'] and 'UveVirtualMachineAgent' in response['value'][k]['value']):
        if (response['value'][k]['value']['UveVirtualMachineAgent']['vm_name'] is not None):
          metric.add_sample('cpu_stats_virt_memory', 
          value = response['value'][k]['value']['VirtualMachineStats']['cpu_stats'][0]['virt_memory'], 
          labels = {"vm_name": response['value'][k]['value']['UveVirtualMachineAgent']['vm_name'] })
        else:
          metric.add_sample('cpu_stats_virt_memory_'+response['value'][k]['name'], 
          value = response['value'][k]['value']['VirtualMachineStats']['cpu_stats'][0]['virt_memory'], 
          labels = {"vm_name": response['value'][k]['name'] })
    yield metric


    


if __name__ == '__main__':
  # Usage python file.py port endpoint
  registry = CollectorRegistry()
  registry.register(JsonCollector('10.60.17.231'))
  start_http_server(9102, registry=registry) 
  while True: time.sleep(1)
