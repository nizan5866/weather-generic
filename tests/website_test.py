#!/bin/bash
import unittest
import requests

class TestBackEnd(unittest.TestCase):
    
    __URL: str = "http://127.0.0.1:5000"
    __DATA_URL:str = "http://127.0.0.1:5000/get_data"
    __HEADERS: dict = {"Content-Type": "application/json"}
    
    def setUp(self) -> None:
        self.data = {"location": "London"}

    def tearDown(self) -> None:
        del self.data
    
    def test_landing_page(self):
        res = requests.get(type(self).__URL)
        self.assertEqual(res.status_code,200)

    def test_get_data1(self):
        """checking normal input"""
        res1 = requests.post(url=type(self).__DATA_URL, json=self.data, headers=type(self).__HEADERS)
        self.assertTrue(res1.json()["status"])

    def test_get_data2(self):
        """checking hebrew input"""
        self.data["location"] = "ירושלים"
        res1 = requests.post(url=type(self).__DATA_URL,json=self.data, headers=type(self).__HEADERS)
        self.assertTrue(res1.json()["status"])
    
    def test_get_data3(self):
        """checking no input"""
        self.data["location"] = ""
        res1 = requests.post(url=type(self).__DATA_URL,json=self.data, headers=type(self).__HEADERS)
        self.assertFalse(res1.json()["status"])
    
    def test_get_data4(self):
        """checking jibrish input"""
        self.data["location"] = "dkfh3487yfho3cy#$%#$%"
        res1 = requests.post(url=type(self).__DATA_URL,json=self.data, headers=type(self).__HEADERS)
        self.assertFalse(res1.json()["status"])
    
    def test_get_data5(self):
        """checking tab"""
        self.data["location"] = "    "
        res1 = requests.post(url=type(self).__DATA_URL,json=self.data, headers=type(self).__HEADERS)
        self.assertFalse(res1.json()["status"])
    
    def test_get_data6(self):
        """checking tab \\t"""
        self.data["location"] = "\t"
        res1 = requests.post(url=type(self).__DATA_URL,json=self.data, headers=type(self).__HEADERS)
        self.assertFalse(res1.json()["status"])
    
    def test_get_data7(self):
        """checking backslashes"""
        self.data["location"] = "\\\\\\"
        res1 = requests.post(url=type(self).__DATA_URL,json=self.data, headers=type(self).__HEADERS)
        self.assertFalse(res1.json()["status"])
    
    def test_get_data8(self):
        """checking enter \\n"""
        self.data["location"] = "\n"
        res1 = requests.post(url=type(self).__DATA_URL,json=self.data, headers=type(self).__HEADERS)
        self.assertFalse(res1.json()["status"])
    
    def test_get_data9(self):
        """checking with empty body"""
        self.data = {}
        res1 = requests.post(url=type(self).__DATA_URL,json=self.data, headers=type(self).__HEADERS)
        self.assertFalse(res1.json()["status"])
    
    def test_get_data10(self):
        """checking multi locations"""
        self.data["location"] = "London/Jerusalem"
        res1 = requests.post(url=type(self).__DATA_URL,json=self.data, headers=type(self).__HEADERS)
        self.assertFalse(res1.json()["status"])

    def test_get_data11(self):
       """checking country"""
       self.data["location"] = "Israel"
       res1 = requests.post(url=type(self).__DATA_URL,json=self.data, headers=type(self).__HEADERS)
       self.assertTrue(res1.json()["status"])
    
    def test_page_not_found(self):
        res = requests.get(type(self).__URL + "/fake_location")
        self.assertEqual(res.json()["message"],"page not found")



if __name__=="__main__":
    unittest.main()
