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

## Upload Template UI
@app.route('/upload/image/', methods=['GET'])
def face_upload_file():
    return render_template('upload.html')

## Upload image to GridFS
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
                # imageformat = Image.open(destination)
                # app.logger.info('%s is the image format', imageformat)
                if filetype is None:
                    ### TODO - add logic to identify truly SVG files
                    ###
                    ###
                    # if (octets.startswith(b'<') and
                    #     b'<svg' in octets[:200] and
                    #     octets.rstrip().endswith(b'svg')):
                    filetype = 'svg'
                localcontenttype = "image/" + filetype
                fs.put(contents, content_type=localcontenttype, filename=filename)
                face_db_table.insert({'face_image': filename})   #insert into database mongo db
        
        responsedata = {'success':'Image Upload Successfully'}        
        response = app.response_class(response=json.dumps(responsedata),
                                  status=200,
                                  mimetype='application/json')        
        return response

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
        
        ##if imageformat != 'jpeg' or imageformat != 'jpg' or imageformat != 'gif' or imageformat != 'png' or imageformat != 'svg':
        if imageformat in ['jpeg', 'jpg', 'gif', 'png', 'svg']:
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
            responsedata = {'response':'Image Format or original file is SVG, not supported'}        
            response = app.response_class(response=json.dumps(responsedata),
                                  status=200,
                                  mimetype='application/json')        
            return response


        if imageformat == 'jpg':
            ## TODO - get a different parser library other than PIL
            #read image file string data
            filestr = f.read()
            tempBuff = io.BytesIO()
            tempBuff.write(filestr)
            tempBuff.seek(0) #need to jump back to the beginning before handing it off to PIL
            # Image.open(tempBuff)
            # print(filestr)
            #convert string data to numpy array
            # npimg = numpy.frombuffer(filestr, numpy.uint8)
            # print('npimg is')
            # print(npimg)
            # # convert numpy array to image
            # img = cv2.imdecode(npimg, cv2.IMREAD_UNCHANGED)
            # if img is None:
            #     print('img is')
            #     print(img)
            #     responsedata = {'response':'error converting image'}        
            #     response = app.response_class(response=json.dumps(responsedata),
            #                       status=500,
            #                       mimetype='application/json')        
            #     return response
                
            # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            
            image = Image.open(tempBuff)
            cfilename = os.path.splitext(f.filename)[0]
            cfilename = cfilename + '.' + imageformat
            print(cfilename)
            img_io = io.BytesIO()
            rgb_im = image.convert('RGB')
            rgb_im.save(img_io, 'JPEG')
            img_io.seek(0)
            # image.save(img_io, imageformat)
            # response = make_response(rgb_im.save(cfilename))
            response = send_file(img_io, as_attachment=True, attachment_filename=cfilename)
            response.mimetype = 'image/' + imageformat
            response.headers.set('Content-Disposition', 'attachment', filename=cfilename)
            return response

        app.logger.info('%s filename', f.filename)
        response = make_response(f.read())
        response.mimetype = f.contentType ## 'image/jpeg'
        response.headers.set('Content-Disposition', 'attachment', filename=f.filename)
        return response

## Transform image to a given image format 

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)


# if __name__ == '__main__':
#     # app.run(port=5002, debug=True)

#     # Serve the app with gevent
#     http_server = WSGIServer(('', 5000), app)
#     http_server.serve_forever()