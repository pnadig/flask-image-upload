FROM python:3.5-jessie

# ENV http_proxy http://proxy-chain.xxx.com:911/
# ENV https_proxy http://proxy-chain.xxx.com:912/

RUN apt-get update

WORKDIR /root
#RUN mkdir flask-mongodb-example
COPY ./ ./
COPY ./templates/* ./templates/
#COPY ./python/* ./flask-mongodb-example/


# System packages 
RUN apt-get update && apt-get install -y curl

# Install miniconda to /miniconda
RUN curl -LO http://repo.continuum.io/miniconda/Miniconda-latest-Linux-x86_64.sh
RUN bash Miniconda-latest-Linux-x86_64.sh -p /miniconda -b
RUN rm Miniconda-latest-Linux-x86_64.sh
ENV PATH=/miniconda/bin:${PATH}
RUN conda update -y conda

# Python packages from conda
# RUN conda install -c conda-forge -y \
#     pymongo \
#     Flask \
#     flasgger

# RUN conda install -c sci-bots -y paho-mqtt

RUN ls -l

RUN pip install -qr ./requirements.txt

ENTRYPOINT ["python", "./server.py"]
EXPOSE 5000