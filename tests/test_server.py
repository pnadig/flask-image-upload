import os, io
import unittest
# from server import app
# from config import test_config

from flask import url_for, Flask
from PIL import Image

# app = Flask(__name__)

class TestMain(unittest.TestCase):
 
####################
#### unit tests ####
####################
 
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

    def test_image_upload(self):
        # Use Flask's test client for our test.
        # self.test_app = app.test_client()
        data = (io.BytesIO('temp.jpg'))

        # Make a test request to the conference app, supplying a fake From phone
        # number
        response = self.client.post('/upload/image/', data=data, follow_redirects=True,
        content_type='multipart/form-data')

        # Assert response is 200 OK.                                           
        self.assertEquals(response.status, "200 OK")
 
 
if __name__ == "__main__":
    unittest.main()