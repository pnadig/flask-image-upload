import os, json, time, io
import unittest

from pymongo import MongoClient, errors
from flask import url_for, Flask
from PIL import Image
from server import app
from config import test_config
import gridfs
from gridfs import NoFile, GridFS
import uuid
from datetime import datetime
from bson.objectid import ObjectId

APP_ROOT = os.path.dirname(os.path.abspath(__file__))


class TestMain(unittest.TestCase):

    ## SETUP TEST
    def setUp(self):
        #self.app = create_app()                                                 
        self.app_context = app.test_request_context()                      
        self.app_context.push()                                                 
        self.client = app.test_client() 

    ## TEST Mongo Setup
    def test_mongo_development(self):
        #self.client = app.test_client()  # we instantiate a flask test client
        time.sleep(5) # hack for the mongoDb database to get running

        face_db_table = MongoClient(test_config['db']['url']).imagesdb_test.faces  # database collection name
        gridfs_db = MongoClient(test_config['db']['url']).imagesdb_test
        test_db_table = MongoClient(test_config['db']['url']).imagesdb_test.test  # database collection name

        fs = gridfs.GridFS(gridfs_db)

        testval = str(uuid.uuid4())
        inserted_id = MongoClient(test_config['db']['url']).imagesdb_test.test.insert_one({
            'testedAt': datetime.now(),
            'testval': testval
        }).inserted_id
        self.assertTrue(MongoClient(test_config['db']['url']).imagesdb_test.name == 'imagesdb_test')
        self.assertTrue(MongoClient(test_config['db']['url']).imagesdb_test.test.find_one({'testval': testval})['testval'] == testval)
        self.assertTrue(MongoClient(test_config['db']['url']).imagesdb_test.test.find_one({'_id': inserted_id})['testval'] == testval)

    ## Test GridFS Insert
    def test_mongo_gridfs_insert(self):
        time.sleep(5) # hack for the mongoDb database to get running

        face_db_table = MongoClient(test_config['db']['url']).imagesdb_test.faces  # database collection name
        gridfs_db = MongoClient(test_config['db']['url']).imagesdb_test
        test_db_table = MongoClient(test_config['db']['url']).imagesdb_test.test  # database collection name

        fs = gridfs.GridFS(gridfs_db)

        destination = APP_ROOT + '/temp1.jpg'
        filename = 'temp1.jpg'
        with open(destination, 'rb') as myimage:
                contents = myimage.read()
                localcontenttype = "image/jpeg"
                inserted_id = fs.put(contents, content_type=localcontenttype, filename=filename)

                fsobject = ObjectId(inserted_id)
                # fsobject = fs.get(fsobject)
                try:
                    f = fs.get(fsobject)
                except NoFile:
                    raise ValueError("File not found!")

                self.assertEqual(f.filename, filename)  

 
    ## Test Image Upload 
    def test_image_upload(self):                   
        with open(APP_ROOT + '/temp1.jpg', 'rb') as img1:
            img1StringIO = io.BytesIO(img1.read())
            filename = 'temp1.jpg'
            #data['file'] = (img1, img1.name)

            response =  self.client.post('/upload/image/',                      
                                    content_type='multipart/form-data',
                                    data={'file': (img1StringIO, filename)},
                                    follow_redirects=True)                        
            #print(response.data)
            self.assertEqual(response.status, '200 OK')  



if __name__ == "__main__":
    unittest.main()