FROM python:3.6.5-slim
COPY ./control-node-exporter.py / 
EXPOSE 9101
RUN pip install -U prometheus_client requests
RUN apt update -y
RUN apt install -y  vim
RUN apt install -y net-tools
CMD [ "python", "/control-node-exporter.py"]
