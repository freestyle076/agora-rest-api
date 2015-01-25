import unittest
import requests
import json


class FilterPostTest(unittest.TestCase):
    def __init__(keyword,category,max_price,min_price,free):
        self.keyword = keyword
        self.category = category
        self.max_price = max_price
        self.min_price = min_price
        self.free = free
    def runTest(self):
        url = "http://147.222.165.3:8000/postquery/"
        payload = {'category':category,'keyword':keyword,'max_price':max_price,"min_price":min_price,"free":free}
        headers = {'content-type': 'application/json','accept':'application/json'}
        r = requests.post(url,data=json.dumps(payload),headers=headers)
        print r.json()
        
test_case = FilterPostTest()
test_case.test_filter_post_list("","","","","0")