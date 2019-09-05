import sys
import time
from xml.dom import minidom
import json, re
import requests
from prometheus_client import start_http_server, Metric, REGISTRY, CollectorRegistry

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
      svc_uve_description = ''
      
      # Add metric system_mem_usage_used
      
      # metric = Metric('contrail_status', '', 'gauge')
      for i in range(number_node):
        current_json_node = json_all_node[i]['value']
        if ('NodeStatus' in current_json_node and 'process_info' in current_json_node['NodeStatus']):
          current_metric = current_json_node['NodeStatus']['process_info']
          for k in range(len(current_metric)):
            # svc_status = 'active' if current_metric[k]['process_state'] == 'PROCESS_STATE_RUNNING' else 'inactive'
            svc_uve_status = None
            svc_uve_description = None
            arp = {
              'server211': '10.60.17.241',
              'server212': '10.60.17.242',
              'server213': '10.60.17.243',
            }
            IntrospectPortMap = {
              "contrail-vrouter-agent" : 8085,
              "contrail-control" : 8083,
              "contrail-collector" : 8089,
              "contrail-query-engine" : 8091,
              "contrail-analytics-api" : 8090,
              "contrail-dns" : 8092,
              "contrail-api" : 8084,
              "contrail-api:0" : 8084,
              "contrail-schema" : 8087,
              "contrail-svc-monitor" : 8088,
              "contrail-device-manager" : 8096,
              "contrail-config-nodemgr" : 8100,
              "contrail-analytics-nodemgr" : 8104,
              "contrail-vrouter-nodemgr" : 8102,
              "contrail-control-nodemgr" : 8101,
              "contrail-database-nodemgr" : 8103,
              "contrail-storage-stats" : 8105,
              "contrail-ipmi-stats" : 8106,
              "contrail-inventory-agent" : 8107,
              "contrail-alarm-gen" : 5995,
              "contrail-alarm-gen:0" : 5995,
              "contrail-snmp-collector" : 5920,
              "contrail-topology" : 5921,
              "contrail-discovery" : 5997,
              "contrail-discovery:0" : 5997,
            }
            BackupImplementedProcesses = {
              'contrail-schema',
              'contrail-svc-monitor',
              'contrail-device-manager'
            }
            # Get node name, process name, process state from TF analytics
            node = re.sub('.local','',json_all_node[i]['name'])
            process_name = current_metric[k]['process_name']
            process_state = current_metric[k]['process_state']

            # If container is running
            if (process_state == 'PROCESS_STATE_RUNNING'):
              svc_status = 'active'
            else:
              svc_status = 'inactive'
            # If service have an introspect port
            if (process_name in IntrospectPortMap and svc_status == 'active'):
              url = 'http://'+ str(arp[node]) + ':' + str(IntrospectPortMap[process_name]) + '/Snh_SandeshUVECacheReq?tname=NodeStatus'
              try:
                # Get introspect service content xml 
                xml = minidom.parseString(requests.get(url).content.decode('UTF-8'))
                # Check NodeStatus not found
                if (not xml.getElementsByTagName('NodeStatus').length ):
                  svc_uve_status = None
                else:
                  node_status = xml.getElementsByTagName('NodeStatus')[0]
                  # Check ProcessStatus not present in NodeStatusUVE
                  if (not node_status.getElementsByTagName('process_status')):
                    svc_uve_status = None
                  # Check Empty ProcessStatus in NodeStatusUVE
                  elif (node_status.getElementsByTagName('process_status').length == 0):
                    svc_uve_status = None
                  else:
                    svc_uve_status = xml.getElementsByTagName('state')[0].firstChild.data
                # svc_uve_status = xml.getElementsByTagName('state')[0].firstChild.data
                # print(svc_uve_status)
              # If connection error
              except (requests.exceptions.ConnectionError) as e:
                # print('Socket Connection error : %s' % (str(e)))
                svc_uve_status = 'connection-error'
                # print(svc_uve_status)
              # If connection timeout
              except requests.exceptions.Timeout as e:
                svc_uve_status = 'connection-timeout'
                # print(svc_uve_status)
              # match all request error
              except requests.exceptions.RequestException as e:
                print(e)

              if svc_uve_status is not None:
                if svc_uve_status == 'Non-Functional':
                  svc_status = 'initializing'
                elif svc_uve_status == 'connection-error':
                  if process_name in BackupImplementedProcesses:
                    svc_status = 'backup'
                  else:
                    svc_status = 'initializing'
                elif svc_uve_status == 'connection-timeout':
                  svc_status = 'timeout'
                elif svc_uve_status == 'Functional':
                  svc_status = 'active'
              else:
                svc_status = 'initializing'
              description = None
              des_xml = xml.getElementsByTagName('description')
              des_xml = des_xml[des_xml.length - 1]
              if (des_xml.firstChild is not None):
                des_xml = des_xml.firstChild.nodeValue
              else:
                des_xml = 'None'
              svc_uve_description = des_xml
              # if svc_uve_description is not None and svc_uve_description is not '':
              #   svc_status = svc_status + ' (' + svc_uve_description + ')'
              values_mapping = {
                'inactive': 0,
                'timeout': 1,
                'initializing': 2,
                'backup': 3,
                'active': 4
              }
            print(str(svc_uve_description))
            metric.add_sample('contrail_status', value = values_mapping[svc_status], labels = {
                'process_name': current_metric[k]['process_name'],
                'process_state': process_state,
                'last_start_time': current_metric[k]['last_start_time'],
                'node': node,
                'node_type': re.sub(r'[:-]', '_', self._node[j]),
                'description': str(svc_uve_description)
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
  registry.register(ClusterCollector('10.60.17.231',['database-node', 'analytics-node', 'config-database-node', 'control-node', 'config-node']))
  start_http_server(9106, registry=registry)
  while True: time.sleep(1)
