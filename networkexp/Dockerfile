FROM python:3.6.5-slim
COPY ./virtual-network-tf-exporter.py / 
EXPOSE 9103
RUN pip install -U prometheus_client requests
RUN apt update -y 
RUN apt install -y  vim 
RUN apt install -y net-tools
CMD [ "python", "/virtual-network-tf-exporter.py"]
