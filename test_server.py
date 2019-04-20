import os, json, time, io
import unittest
# from server import app
# from config import test_config
from pymongo import MongoClient, errors
from flask import url_for, Flask
from PIL import Image
from server import app
from config import test_config
import gridfs
from gridfs import NoFile, GridFS

app = Flask(__name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))


class TestMain(unittest.TestCase):
 
####################
#### unit tests ####
####################

    # this method is run before each test
    def setUp(self):
        #self.app = create_app()                                                 
        self.app_context = app.test_request_context()                      
        self.app_context.push()                                                 
        self.client = app.test_client() 

        #self.client = app.test_client()  # we instantiate a flask test client
        time.sleep(5) # hack for the mongoDb database to get running

        face_db_table = MongoClient(test_config['db']['url']).imagesdb_test.faces  # database collection name
        gridfs_db = MongoClient(test_config['db']['url']).imagesdb_test

        fs = gridfs.GridFS(gridfs_db)

        # db.create_all()  # create the database objects
        # # add some fixtures to the database
        # self.user = User(
        #     email='joe@theodo.fr',
        #     password='super-secret-password'
        # )
        # db.session.add(self.user)
        # db.session.commit()
 
    # def test_image_upload(self):
    #     payload = <some_payload_here>
	#     resp = self.client.post(url_for('<module_name>.log_message', level='debug'),
	#                             data=json.dumps(payload), content_type='application/json')
	#     # or you can do it this way too (its your option which one is better)
	#     resp = self.client.post('/environment/debug', data=json.dumps(payload),
	#                             content_type='application/json')
	#     self.assertEqual(resp.data, <valid resp data>)
    #     # response = self.app.get('/', follow_redirects=True)
    #     self.assertEqual(response.resp, 200)

    # def test_image_upload(self):
    #     # Use Flask's test client for our test.
    #     self.test_app = app.test_client()
    #     data = dict(logo=(io.BytesIO(b'This is test'), 'temp1.jpg'))
    #     response = self.test_app.post('/upload/image/', 
    #             data=data,buffered=True,
    #             follow_redirects=True, content_type='multipart/form-data')
    #     self.assertEqual(response.status, '200')

    # def test_image_upload(self):
    #     #self.test_app = app.test_client()
    #     with open(APP_ROOT + '/temp1.jpg', 'rb') as img1:
    #         img1StringIO = io.BytesIO(img1.read())
    #     # img1StringIO.seek(0)
    #     # print(img1StringIO)
    #     response = self.client.post('/upload/image/',
    #                             content_type='multipart/form-data',
    #                             data={'face_image': (img1StringIO, 'temp1.jpg')},
    #                             follow_redirects=True)
    #     print(response)                        
    #     ##self.assertEqual(response.status, '200')                                 


    # def test_hello(self):
    #     # rv = self.app.post('/add', data=dict(
    #     #                        file=(io.BytesIO(b"this is a test"), 'test.pdf'),
    #     #                    ), follow_redirects=True)
    #     # print(rv)                   
    #     with open(APP_ROOT + '/temp1.jpg', 'rb') as img1:
    #         img1StringIO = io.BytesIO(img1.read())
    #         #data['file'] = (img1, img1.name)

    #         response =  self.client.post('/upload/image/',                      
    #                                 content_type='multipart/form-data',
    #                                 data={'face_image': (img1StringIO, 'temp1.jpg')},
    #                                 follow_redirects=True)                        

    #         self.assertEqual(response.status, '200')  

    def test_add_opportunity_attachment(self):
        payload = {"title": "Testing upload image", "description": "Testing upload image description"}
        with open(APP_ROOT + '/temp1.jpg', 'rb') as file_contents:
            files = {'file': ('temp1.jpg', file_contents)}
            headers = {'Content-Type': 'image/jpeg', "enctype": "multipart/form-data", "Content-Disposition":"attachment;filename=temp1.jpg"}
            #response = self.client.post('/upload/image/', data=payload, content_type='multipart/form-data',headers=headers)
            response =self.session.post('/upload/image/', files=files, data=payload)
            self.assertEqual(response.status, '200')   
 
 
if __name__ == "__main__":
    unittest.main()