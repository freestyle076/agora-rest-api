import unittest
import requests
import json

class FilterPostTest(unittest.TestCase):
    def setUp(self):
        self.url = "http://147.222.165.3:8000/postquery/"
        self.headers = {'content-type': 'application/json','accept':'application/json'}
        
    def test_categories_filter_clothing(self):
        
        print "\nTesting results returned by query for - Category: Clothing"
        base_category = "Clothing"
        payload = {'categories':base_category,'keywordSearch':'','max_price':'',"min_price":'',"free":'0'}
        r = requests.post(self.url,data=json.dumps(payload),headers=self.headers)
        
        for post in r.json()['posts']:
            test_category = post['category']
            self.assertEquals(base_category,test_category)
        
    def test_categories_filter_electronics(self):

        print "\nTesting results returned by query for - Category: Electronics"
        base_category = "Electronics"
        payload = {'categories':base_category,'keywordSearch':'','max_price':'',"min_price":'',"free":'0'}
        r = requests.post(self.url,data=json.dumps(payload),headers=self.headers)        

        for post in r.json()['posts']:
            test_category = post['category']
            self.assertEquals(base_category,test_category)
            
    def test_categories_filter_household(self):
            
        print "\nTesting results returned by query for - Category: Household"
        base_category = "Household"
        payload = {'categories':base_category,'keywordSearch':'','max_price':'',"min_price":'',"free":'0'}
        r = requests.post(self.url,data=json.dumps(payload),headers=self.headers)        
        
        for post in r.json()['posts']:
            test_category = post['category']
            self.assertEquals(base_category,test_category)
            
    def test_categories_filter_recreation(self):
            
        print "\nTesting results returned by query for - Category: Recreation"
        base_category = "Recreation"
        payload = {'categories':base_category,'keywordSearch':'','max_price':'',"min_price":'',"free":'0'}
        r = requests.post(self.url,data=json.dumps(payload),headers=self.headers)        
        
        for post in r.json()['posts']:
            test_category = post['category']
            self.assertEquals(base_category,test_category)
        
    def test_categories_filter_books(self):
        
        print "\nTesting results returned by query for - Category: Books"
        base_category = "Books"
        payload = {'categories':base_category,'keywordSearch':'','max_price':'',"min_price":'',"free":'0'}
        r = requests.post(self.url,data=json.dumps(payload),headers=self.headers)        
        
        for post in r.json()['posts']:
            test_category = post['category']
            self.assertEquals(base_category,test_category)
            
    def test_categories_filter_rideshares(self):

        print "\nTesting results returned by query for - Category: Ride Shares"
        base_category = "Ride Shares"
        payload = {'categories':base_category,'keywordSearch':'','max_price':'',"min_price":'',"free":'0'}
        r = requests.post(self.url,data=json.dumps(payload),headers=self.headers)        
        
        for post in r.json()['posts']:
            test_category = post['category']
            self.assertEquals(base_category,test_category)
            
            
    def test_categories_filter_services(self):
    
        print "\nTesting results returned by query for - Category: Services"
        base_category = "Services"
        payload = {'categories':base_category,'keywordSearch':'','max_price':'',"min_price":'',"free":'0'}
        r = requests.post(self.url,data=json.dumps(payload),headers=self.headers)        
        
        for post in r.json()['posts']:
            test_category = post['category']
            self.assertEquals(base_category,test_category)
            
    def test_categories_filter_events(self):
            
        print "\nTesting results returned by query for - Category: Events"
        base_category = "Events"
        payload = {'categories':base_category,'keywordSearch':'','max_price':'',"min_price":'',"free":'0'}
        r = requests.post(self.url,data=json.dumps(payload),headers=self.headers)        
        
        for post in r.json()['posts']:
            test_category = post['category']
            self.assertEquals(base_category,test_category)
        
        
if __name__ == '__main__':
    unittest.main()
