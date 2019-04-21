FROM python:3.5-jessie

# ENV http_proxy http://proxy-chain.xxx.com:911/
# ENV https_proxy http://proxy-chain.xxx.com:912/

RUN apt-get update

WORKDIR /root

RUN mkdir server
COPY ./ ./server/
COPY ./server/* ./server/
COPY ./server/templates/* ./server/templates/
#COPY ./python/* ./flask-mongodb-example/


# System packages 
RUN apt-get update && apt-get install -y curl

RUN ls -l ./server

RUN pip install -qr ./server/requirements.txt

ENTRYPOINT ["python", "./server/server.py"]
EXPOSE 5000