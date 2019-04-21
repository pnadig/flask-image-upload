### Image Upload and Image Conversion Microservices with Flask, MongoDB and Docker-compose
* Docker Compose with nginx reverse proxy
* Images saved on Gridfs MongoDB
* Python Flask Microservices for image upload service
* Python Flask Microservices for image conversion services
* Python unittests for each endpoint


### Branch out from:
#### Branch 1. master
Run

```
python server.py

to run unit tests:
python test_server.py

```


#### Branch 2. microservices

Run

```
docker-compose up

endpoints:
To Upload Image
http://$host/upload/image/

To retrieve Image
http://$host:81/image/<fileid>/

To convert Image to jpg/jpeg
http://$host:82/image/<fileid>/<jpeg|jpg>

To convert Image to png
http://$host:83/image/<fileid>/<png>

To convert Image to gif
http://$host:84/image/<fileid>/<gif>

```


#### Branch 3. gRPC protoc image conversion idiomatic library
##### TODO