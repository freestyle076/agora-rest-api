import requests
import json
from models import User
import unittest

class TestUserFunctions(unittest.TestCase):
    def test_create_user(self):
        data = {'username':'aturing','phone':'5098675309','first_name':"Alan",'last_name': "Turing","gonzaga_email":"Turing@gonzaga.edu","pref_email":"TuringTest@gmail.com"}
        headers = {'content-type':'application/json'}
        r = requests.post("http://147.222.165.3:8000/createuser/",data=json.dumps(data),headers=headers)
        new_user = User.objects.get(username='aturing')
        self.assertEqual('5098675309',new_user.phone)
        self.assertEqual('Alan',new_user.first_name)
        self.assertEqual('Turing',new_user.last_name)
    
    
if __name__ == '__main':
    unittest.main()