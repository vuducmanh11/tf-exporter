docker build -t tf-cluster -f Dockerfile .
docker tag  tf-cluster 10.240.201.50:8891/prometheus_tf_cluster_exporter
docker push 10.240.201.50:8891/prometheus_tf_cluster_exporter
