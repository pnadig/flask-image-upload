from flask import Flask, redirect, url_for, request, render_template, Response, make_response, jsonify, send_file
from werkzeug.utils import secure_filename
import os, json, time, io
import gridfs
from gridfs import NoFile, GridFS
from pymongo import MongoClient, errors
from bson.objectid import ObjectId
from gevent.pywsgi import WSGIServer
import imghdr
from config import config
from PIL import Image
import numpy
import cv2
import six
# try:
#     from StringIO import StringIO
# except ImportError:
#     from io import StringIO

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

time.sleep(5) # hack for the mongoDb database to get running

face_db_table = MongoClient(config['db']['url']).imagesdb.faces  # database collection name
gridfs_db = MongoClient(config['db']['url']).imagesdb


# face_db_table = MongoClient('localhost', 32768).imagesdb.faces  # database collection name
# gridfs_db = MongoClient('localhost', 32768).imagesdb

fs = gridfs.GridFS(gridfs_db)

## Download/Retrieve image from Mongo GridFS given fileID
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

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    ##app.run(debug=True, host='0.0.0.0', port=port)
    app.run(host='0.0.0.0', port=port)
