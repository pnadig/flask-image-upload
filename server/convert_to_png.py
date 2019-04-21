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

## Download/Retrieve image from Mongo GridFS given fileID and imageFormat
@app.route('/image/<fileid>/<imageformat>', methods=['GET'])
def convert_image(fileid,imageformat):    
    if request.method == 'GET':
        app.logger.info('%s is image format \n', imageformat)
        fsobject = ObjectId(fileid)
        # fsobject = fs.get(fsobject)
        try:
            f = fs.get(fsobject)
        except NoFile:
            raise ValueError("File not found!")
        
        ## SUPPORTED image formats:
        if imageformat in ['png','svg']:
            print('file format supported')
        else:
        ##if imageformat != ('jpeg' or 'jpg' or 'gif' or 'png' or 'svg'):    
            responsedata = {'response':'Image Format Not Supported'}        
            response = app.response_class(response=json.dumps(responsedata),
                                  status=404,
                                  mimetype='application/json')        
            return response

        if (imageformat == 'svg') or (f.contentType == 'image/svg'):
            ## TODO - get a different parser library other than PIL
            responsedata = {'response':'requested Image Format or original file is SVG, not supported'}        
            response = app.response_class(response=json.dumps(responsedata),
                                  status=200,
                                  mimetype='application/json')        
            return response


        if imageformat == 'png' :
            filestr = f.read()
            tempBuff = io.BytesIO()
            tempBuff.write(filestr)
            tempBuff.seek(0) #need to jump back to the beginning before handing it off to PIL
            image = Image.open(tempBuff)
            cfilename = os.path.splitext(f.filename)[0]
            cfilename = cfilename + '.' + imageformat
            print(cfilename)
            img_io = io.BytesIO()
            rgb_im = image.convert('RGB')
            rgb_im.save(img_io, 'PNG')
            img_io.seek(0)
            response = send_file(img_io, as_attachment=True, attachment_filename=cfilename)
            response.mimetype = 'image/' + imageformat
            response.headers.set('Content-Disposition', 'attachment', filename=cfilename)
            return response

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    ##app.run(debug=True, host='0.0.0.0', port=port)
    app.run(host='0.0.0.0', port=port)
