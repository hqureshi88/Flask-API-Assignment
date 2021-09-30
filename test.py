# try:
from app import app
import unittest
# except Exception as e:
#     print("Some modules are missing {}".format(e))

class FlaskTest(unittest.TestCase):
    # check for response 200
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get("/")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)


    # check if content return is application/json
    # def test_index_content(self):
    #     tester = app.test_client(self)
    #     response = tester.get("/")
    #     statuscode = response.status_code
    #     self.assertEqual(response.content_type, "application/json")
    
    # check for Data returned
    def test_index_content(self):
        tester = app.test_client(self)
        response = tester.get("/", content_type="html/text")
        self.assertTrue(b'name' in response.data)

if __name__ == "__main__":
    unittest.main()