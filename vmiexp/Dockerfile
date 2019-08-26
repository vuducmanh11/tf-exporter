FROM python:3.7-slim
COPY ./virtual-machine-interface-exporter.py / 
EXPOSE 9105
RUN pip install -U prometheus_client requests
RUN apt update -y
RUN apt install -y  vim 
RUN apt install -y net-tools
CMD [ "python", "/virtual-machine-interface-exporter.py"]
