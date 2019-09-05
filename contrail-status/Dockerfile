FROM python:3.7-slim
COPY ./contrail-status.py / 
EXPOSE 9103
RUN pip install -U prometheus_client requests 
RUN apt update -y 
RUN apt install -y  vim 
RUN apt install -y net-tools
CMD [ "python", "/contrail-status.py"]
