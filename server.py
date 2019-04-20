from flask import Flask, redirect, url_for, request, render_template, Response, make_response
from werkzeug.utils import secure_filename
import os, json, time
import gridfs
from gridfs import NoFile, GridFS
from pymongo import MongoClient, errors
from bson.objectid import ObjectId
from gevent.pywsgi import WSGIServer
import imghdr
from config import config


app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

time.sleep(5) # hack for the mongoDb database to get running

face_db_table = MongoClient(config['db']['url']).imagesdb.faces  # database collection name
gridfs_db = MongoClient(config['db']['url']).imagesdb


# face_db_table = MongoClient('localhost', 32768).imagesdb.faces  # database collection name
# gridfs_db = MongoClient('localhost', 32768).imagesdb

fs = gridfs.GridFS(gridfs_db)

@app.route('/upload/image/', methods=['GET'])
def face_upload_file():
    return render_template('upload.html')


@app.route('/upload/image/', methods=['POST'])
def image_upload():
    target = os.path.join(APP_ROOT, 'face-images/')  #folder path
    if not os.path.isdir(target):
            os.mkdir(target)     # create folder if not exits
    
    if request.method == 'POST':
        for upload in request.files.getlist("face_image"): #multiple image handle
            filename = secure_filename(upload.filename)
            destination = "/".join([target, filename])
            upload.save(destination)
            with open(destination, 'rb') as myimage:
                contents = myimage.read()
                app.logger.info('%s filename', destination)
                filetype = imghdr.what(destination)
                app.logger.info('%s is the image type', filetype)
                if filetype is None:
                    ### TODO - add logic to identify truly SVG files
                    # if (octets.startswith(b'<') and
                    #     b'<svg' in octets[:200] and
                    #     octets.rstrip().endswith(b'</svg>')):
                    filetype = 'svg'
                localcontenttype = "image/" + filetype
                fs.put(contents, content_type=localcontenttype, filename=filename)
                face_db_table.insert({'face_image': filename})   #insert into database mongo db
                
        return 'Image Upload Successfully'


@app.route('/image/<fileid>', methods=['GET'])
def get_image(fileid):    
    if request.method == 'GET':
        fsobject = ObjectId(fileid)
        # fsobject = fs.get(fsobject)
        try:
            f = fs.get(fsobject)
        except NoFile:
            raise ValueError("File not found!")
              
        app.logger.info('%s filename', f.filename)
        response = make_response(f.read())
        response.mimetype = f.contentType ## 'image/jpeg'
        response.headers.set('Content-Disposition', 'attachment', filename=f.filename)
        return response


      
        ## fsobject = fs.get(fileid).read()
        #return 'Image Retrieved Successfully'
    #return Response('', status=200, mimetype='application/json')    

# if __name__ == '__main__':
#     app.run(host='0.0.0.0')

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)


# if __name__ == '__main__':
#     # app.run(port=5002, debug=True)

#     # Serve the app with gevent
#     http_server = WSGIServer(('', 5000), app)
#     http_server.serve_forever()