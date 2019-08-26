FROM python:3.6.5-slim
COPY ./vm-tf-node-exporter.py / 
EXPOSE 9102
RUN pip install -U prometheus_client requests
RUN apt update -y
RUN apt install -y vim 
RUN apt install -y net-tools
CMD [ "python", "/vm-tf-node-exporter.py"]
