from prometheus_client import start_http_server, Metric, REGISTRY
import json
import requests
import sys
import time
import re

class JsonCollector(object):
    def __init__(self, endpoint):
        self._endpoint = endpoint
    
    def collect(self):
        # fetch JSON response
        virtual_networks = json.loads(requests.get('http://10.60.17.231:8081/analytics/uves/virtual-networks').content.decode('UTF-8'))
        # print(self._endpoint)
        # Create Metric for virtual networks
        virtual_network = virtual_networks[0]
        vn_json = json.loads(requests.get(virtual_network['href']).content.decode('UTF-8'))
        if 'UveVirtualNetworkAgent' in vn_json:
            metric = Metric('net zero' , 'All about virtual_network', 'gauge')
            vn_json = json.loads(requests.get(virtual_network['href']).content.decode('UTF-8'))
            print(vn_json)
            metric.add_sample('out_bandwidth_usage', value=vn_json['UveVirtualNetworkAgent']['out_bandwidth_usage'], labels={})
            metric.add_sample('in_bandwidth_usage', value=vn_json['UveVirtualNetworkAgent']['in_bandwidth_usage'], labels={})
            metric.add_sample('egress_flow_count', value=vn_json['UveVirtualNetworkAgent']['egress_flow_count'], labels={})
            yield metric

        virtual_network = virtual_networks[1]
        vn_json = json.loads(requests.get(virtual_network['href']).content.decode('UTF-8'))
        if 'UveVirtualNetworkAgent' in vn_json:
            metric = Metric('net_one' , 'All about virtual_network', 'gauge')
            vn_json = json.loads(requests.get(virtual_network['href']).content.decode('UTF-8'))
            print(vn_json)
            metric.add_sample('out_bandwidth_usage', value=vn_json['UveVirtualNetworkAgent']['out_bandwidth_usage'], labels={})
            metric.add_sample('in_bandwidth_usage', value=vn_json['UveVirtualNetworkAgent']['in_bandwidth_usage'], labels={})
            metric.add_sample('egress_flow_count', value=vn_json['UveVirtualNetworkAgent']['egress_flow_count'], labels={})
            yield metric

        virtual_network = virtual_networks[2]
        vn_json = json.loads(requests.get(virtual_network['href']).content.decode('UTF-8'))
        if 'UveVirtualNetworkAgent' in vn_json:
            metric = Metric('net_two' , 'All about virtual_network', 'gauge')
            vn_json = json.loads(requests.get(virtual_network['href']).content.decode('UTF-8'))
            print(vn_json)
            metric.add_sample('out_bandwidth_usage', value=vn_json['UveVirtualNetworkAgent']['out_bandwidth_usage'], labels={})
            metric.add_sample('in_bandwidth_usage', value=vn_json['UveVirtualNetworkAgent']['in_bandwidth_usage'], labels={})
            metric.add_sample('egress_flow_count', value=vn_json['UveVirtualNetworkAgent']['egress_flow_count'], labels={})
            yield metric

        virtual_network = virtual_networks[3]
        vn_json = json.loads(requests.get(virtual_network['href']).content.decode('UTF-8'))
        if 'UveVirtualNetworkAgent' in vn_json:
            metric = Metric('net_three' , 'All about virtual_network', 'gauge')
            vn_json = json.loads(requests.get(virtual_network['href']).content.decode('UTF-8'))
            print(vn_json)
            metric.add_sample('out_bandwidth_usage', value=vn_json['UveVirtualNetworkAgent']['out_bandwidth_usage'], labels={})
            metric.add_sample('in_bandwidth_usage', value=vn_json['UveVirtualNetworkAgent']['in_bandwidth_usage'], labels={})
            metric.add_sample('egress_flow_count', value=vn_json['UveVirtualNetworkAgent']['egress_flow_count'], labels={})
            yield metric



        # Convert requests to summary in seconds
        #metric = Metric('svc_requests_duration_seconds', 'Requests time taken in seconds', 'summary')
        #metric.add_sample('svc_requests_duration_seconds_count', value=response['requests_handled'], labels={})
        #metric.
        #yield metric

        # Counter for the failures
        #metric = Metric('svc_requests_failed_total', 'Requests failed', 'summary')
        #metric.add_sample('svc_requests_failed_total', value='xxxxxxxx', labels={})

        # Metrics about bandwidth usage
        # metric = Metric('bandwidth_usage', 'bandwidth_usage', 'gauge')
        # metric.add_sample('out_bandwidth_usage', value=response['UveVirtualNetworkAgent']['out_bandwidth_usage'], labels={})
        # metric.add_sample('in_bandwidth_usage', value=response['UveVirtualNetworkAgent']['in_bandwidth_usage'], labels={})
        # yield metric

        # Metrics about all Virtual Network


if __name__ == '__main__':
    # Usage: json_exporter.py port endpoint
    start_http_server(int(sys.argv[1]))
    REGISTRY.register(JsonCollector('http://10.60.17.233:8081/analytics/uves/virtual-network/default-domain:admin:right_vn?flat'))
    while True: time.sleep(1)
