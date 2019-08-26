docker build -t tf-virtual-network -f Dockerfile .
docker tag  tf-virtual-network 10.240.201.50:8891/prometheus_tf_virtual_network_exporter
docker push 10.240.201.50:8891/prometheus_tf_virtual_network_exporter
