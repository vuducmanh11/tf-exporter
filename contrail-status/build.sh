docker build -t tf-status -f Dockerfile .
docker tag  tf-status 10.240.201.50:8891/tf-control-exporter
docker push 10.240.201.50:8891/tf-control-exporter
