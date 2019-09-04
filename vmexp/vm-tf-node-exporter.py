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
    num_vm = len(json_all_vm)
    UveVirtualMachineAgent = {
      "vm_cpu_count": {
        "type": 'gauge',
        "description": 'Number cpu of VM'
      },
      "vm_state": {
        "type": 'string',
        "description": 'State of VM'
      },
      "cpu_info": {
        "type": 'dict',
        "item_dict": {
          "virt_memory": 'not define',
          "cpu_one_min_avg": 'not define',
          "disk_used_bytes": 'not define',
          "vm_memory_quota": 'not define',
          "peak_virt_memory": 'not define',
          "disk_allocated_bytes": 'not define',
          "rss": 'not define',
        }
      
      },

      "vrouter": {
        "type": 'string',
        "description": 'Name server contain VM'
      },
      "interface_list": {
        "type": 'list',
        "description": "List interface of VM",
        "item_list": 'number'
      }
    }

    for name_metric in UveVirtualMachineAgent:
      if UveVirtualMachineAgent[name_metric]['type'] == 'string':
        metric = Metric(name_metric, UveVirtualMachineAgent[name_metric]['description'], 'gauge')
        for i in range(num_vm):
          current_json_vm = json_all_vm[i]['value']
          vm_uuid = json_all_vm[i]['name']
          if ('UveVirtualMachineAgent' in current_json_vm and name_metric in current_json_vm['UveVirtualMachineAgent'] and 'vm_name' in current_json_vm['UveVirtualMachineAgent'] ):
            current_metric = current_json_vm['UveVirtualMachineAgent'][name_metric]
            metric.add_sample(name_metric, value=1, labels={
              name_metric: current_metric,
              "vm_uuid": vm_uuid,
              "vm_name": current_json_vm['UveVirtualMachineAgent']['vm_name']
              })
          elif ('UveVirtualMachineAgent' in current_json_vm and 'vm_name' in current_json_vm['UveVirtualMachineAgent'] and name_metric == 'vm_state'):
            metric.add_sample(name_metric, value=0, labels={
              'vm_state': 'none',
              "vm_uuid": vm_uuid,
              "vm_name": current_json_vm['UveVirtualMachineAgent']['vm_name']
              })
        yield metric
      elif UveVirtualMachineAgent[name_metric]['type'] == 'gauge':
        metric = Metric(name_metric, UveVirtualMachineAgent[name_metric]['description'], 'gauge')
        for i in range(num_vm):
          current_json_vm = json_all_vm[i]['value']
          vm_uuid = json_all_vm[i]['name']
          if ('UveVirtualMachineAgent' in current_json_vm and name_metric in current_json_vm['UveVirtualMachineAgent']):
            current_metric = current_json_vm['UveVirtualMachineAgent'][name_metric]
            metric.add_sample(name_metric, value=current_metric, labels={
              "vm_uuid": vm_uuid,
              "vm_name": current_json_vm['UveVirtualMachineAgent']['vm_name']
              })
        yield metric
      elif UveVirtualMachineAgent[name_metric]['type'] == 'dict':
        for metric_item in UveVirtualMachineAgent[name_metric]['item_dict']:
          metric = Metric(name_metric+'_'+metric_item, UveVirtualMachineAgent[name_metric]['item_dict'][metric_item], 'gauge')
          for i in range(num_vm):
            current_json_vm = json_all_vm[i]['value']
            vm_uuid = json_all_vm[i]['name']
            if ('UveVirtualMachineAgent' in current_json_vm and name_metric in current_json_vm['UveVirtualMachineAgent']):
              current_metric = current_json_vm['UveVirtualMachineAgent'][name_metric]
              metric.add_sample(name_metric+'_'+metric_item, value=current_metric[metric_item], labels={
                "vm_uuid": vm_uuid,
                "vm_name": current_json_vm['UveVirtualMachineAgent']['vm_name']
                })
          yield metric
      elif UveVirtualMachineAgent[name_metric]['type'] == 'list':
        if UveVirtualMachineAgent[name_metric]['item_list'] == 'number':
          metric = Metric(name_metric, UveVirtualMachineAgent[name_metric]['description'], 'gauge')
          for i in range(num_vm):
            current_json_vm = json_all_vm[i]['value']
            vm_uuid = json_all_vm[i]['name']
            if ('UveVirtualMachineAgent' in current_json_vm and name_metric in current_json_vm['UveVirtualMachineAgent']):
              current_metric = current_json_vm['UveVirtualMachineAgent'][name_metric]
              for k in range(len(current_metric)):
                metric.add_sample(name_metric, value=1, labels={
                  "vm_uuid": vm_uuid,
                  "vm_name": current_json_vm['UveVirtualMachineAgent']['vm_name'],
                  name_metric+'_'+str(k): current_metric[k] 
                  })
          yield metric



    # # Add metric cpu_stats_virt_memory
    # metric = Metric('cpu_stats_virt_memory', 'virt memory used by vm', 'gauge')
    
    # for k in range(num_vm):
    #   if ('VirtualMachineStats' in response['value'][k]['value'] and 'UveVirtualMachineAgent' in response['value'][k]['value']):
    #     if (response['value'][k]['value']['UveVirtualMachineAgent']['vm_name'] is not None):
    #       metric.add_sample('cpu_stats_virt_memory', 
    #       value = response['value'][k]['value']['VirtualMachineStats']['cpu_stats'][0]['virt_memory'], 
    #       labels = {"vm_name": response['value'][k]['value']['UveVirtualMachineAgent']['vm_name'] })
    #     else:
    #       metric.add_sample('cpu_stats_virt_memory_'+response['value'][k]['name'], 
    #       value = response['value'][k]['value']['VirtualMachineStats']['cpu_stats'][0]['virt_memory'], 
    #       labels = {"vm_name": response['value'][k]['name'] })
    # yield metric


    # # Add metric cpu_stats_cpu_one_min_avg
    # metric = Metric('cpu_stats_cpu_one_min_avg', 'cpu per one min used by vm', 'gauge')
    
    # for k in range(num_vm):
    #   if ('VirtualMachineStats' in response['value'][k]['value'] and 'UveVirtualMachineAgent' in response['value'][k]['value']):
    #     if (response['value'][k]['value']['UveVirtualMachineAgent']['vm_name'] is not None):
    #       metric.add_sample('cpu_stats_cpu_one_min_avg', 
    #       value = response['value'][k]['value']['VirtualMachineStats']['cpu_stats'][0]['cpu_one_min_avg'], 
    #       labels = {"vm_name": response['value'][k]['value']['UveVirtualMachineAgent']['vm_name'] })
    #     else:
    #       metric.add_sample('cpu_stats_cpu_one_min_avg', 
    #       value = response['value'][k]['value']['VirtualMachineStats']['cpu_stats'][0]['cpu_one_min_avg'], 
    #       labels = {"vm_name": response['value'][k]['name'] })
    # yield metric


    # # Add metric cpu_stats_disk_used_bytes
    # metric = Metric('cpu_stats_disk_used_bytes', 'Disk used by vm (byte) ', 'gauge')
    
    # for k in range(num_vm):
    #   if ('VirtualMachineStats' in response['value'][k]['value'] and 'UveVirtualMachineAgent' in response['value'][k]['value']):
    #     if (response['value'][k]['value']['UveVirtualMachineAgent']['vm_name'] is not None):
    #       metric.add_sample('cpu_stats_disk_used_bytes', 
    #       value = response['value'][k]['value']['VirtualMachineStats']['cpu_stats'][0]['disk_used_bytes'], 
    #       labels = {"vm_name": response['value'][k]['value']['UveVirtualMachineAgent']['vm_name'] })
    #     else:
    #       metric.add_sample('cpu_stats_disk_used_bytes', 
    #       value = response['value'][k]['value']['VirtualMachineStats']['cpu_stats'][0]['disk_used_bytes'], 
    #       labels = {"vm_name": response['value'][k]['name'] })
    # yield metric


    # # Add metric cpu_stats_disk_allocated_bytes
    # metric = Metric('cpu_stats_disk_allocated_bytes', 'disk allocated used by vm (byte) ', 'gauge')
    
    # for k in range(num_vm):
    #   if ('VirtualMachineStats' in response['value'][k]['value'] and 'UveVirtualMachineAgent' in response['value'][k]['value']):
    #     if (response['value'][k]['value']['UveVirtualMachineAgent']['vm_name'] is not None):
    #       metric.add_sample('cpu_stats_disk_allocated_bytes', 
    #       value = response['value'][k]['value']['VirtualMachineStats']['cpu_stats'][0]['disk_allocated_bytes'], 
    #       labels = {"vm_name": response['value'][k]['value']['UveVirtualMachineAgent']['vm_name'] })
    #     else:
    #       metric.add_sample('cpu_stats_disk_allocated_bytes', 
    #       value = response['value'][k]['value']['VirtualMachineStats']['cpu_stats'][0]['disk_allocated_bytes'], 
    #       labels = {"vm_name": response['value'][k]['name'] })
    # yield metric
    


if __name__ == '__main__':
  # Usage python file.py port endpoint
  registry = CollectorRegistry()
  registry.register(JsonCollector('10.60.17.231'))
  start_http_server(9102, registry=registry) 
  while True: time.sleep(1)
