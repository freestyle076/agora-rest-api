import requests
import json
from django.test import TestCase
import unittest
import ast


class TestUserFunctions(unittest.TestCase):

    def test1_create_post(self):
        print "Testing Create Post Function"
        TestUserFunctions.category = "Electronics"
        data = {'username':'tmiller12','description':'Samsung','price':"100.00",'title': "TV","category":TestUserFunctions.category,"gonzaga_email":"0","pref_email":"0","call":"1","text":"1","images":"[]"}
        TestUserFunctions.headers = {'content-type':'application/json'}
        r = requests.post("http://147.222.165.133:8000/createpost/",data=json.dumps(data),headers=TestUserFunctions.headers)
        self.assertEqual(r.status_code,200)
        request_data = ast.literal_eval(r.content) #parse data
        TestUserFunctions.postid = request_data["id"]
        
    def test2_view_post(self):
        print "\nTesting View Post Function"
        data = {'post_id' : str(TestUserFunctions.postid), 'category': TestUserFunctions.category}
        r = requests.post("http://147.222.165.133:8000/viewpost/",data=json.dumps(data),headers=TestUserFunctions.headers)
        request_data2 = ast.literal_eval(r.content) #parse data
        self.assertEqual(r.status_code,200)
        self.assertEqual(request_data2['description'],'Samsung')
        self.assertEqual(request_data2["price"],'100.00')
        self.assertEqual(request_data2["title"],'TV')
        
    def test3_edit_post(self):
        print "\nTesting Edit Post Function"
        data = {'username':'tmiller12','id':str(TestUserFunctions.postid),'description':'Samsung','price':"10.00",'title': "Television","category":TestUserFunctions.category,"gonzaga_email":"0","pref_email":"0","call":"1","text":"1","images":"[]"}
        r = requests.post("http://147.222.165.133:8000/editpost/",data=json.dumps(data),headers=TestUserFunctions.headers)
        self.assertEqual(r.status_code,200)

    def test4_view_post(self):
        print "\nTesting View Post Function After Edit Post"
        data = {'post_id' : str(TestUserFunctions.postid), 'category': TestUserFunctions.category}
        r = requests.post("http://147.222.165.133:8000/viewpost/",data=json.dumps(data),headers=TestUserFunctions.headers)
        request_data2 = ast.literal_eval(r.content) #parse data
        self.assertEqual(r.status_code,200)
        self.assertEqual(request_data2['description'],'Samsung')
        self.assertEqual(request_data2["price"],'10.00')
        self.assertEqual(request_data2["title"],'Television')

        
if __name__ == '__main__':
    unittest.main()