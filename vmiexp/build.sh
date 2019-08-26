docker build -t tf-virtual-interface -f Dockerfile .
docker tag  tf-virtual-interface 10.240.201.50:8891/prometheus_tf_virtual_interface_exporter
docker push 10.240.201.50:8891/prometheus_tf_virtual_interface_exporter
