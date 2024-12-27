import unittest
import requests
import json
import logging

#Mostly the same code as Integration but this is performed with HTTP requests and not ES client.
class TestMelbourneWeatherOperations(unittest.TestCase):
    es_url = 'https://localhost:9200'
    index_name = 'melbourne_weather_test'
    auth = ('elastic', 'password_goes_here')
    doc_id = None  # Class attribute to store document ID

    @classmethod
    def setUpClass(cls):
        cls.delete_index() #Can be commented out to see the doc live in ES
        cls.create_index()

    @classmethod
    def delete_index(cls):
        requests.delete(f"{cls.es_url}/{cls.index_name}", auth=cls.auth, verify=False)

    @classmethod
    def create_index(cls):
        settings = {
            "settings": {
                "number_of_shards": 1,
                "number_of_replicas": 0
            },
            "mappings": {
                "properties": {
                    "station": {"type": "keyword"},
                    "current_date_time": {"type": "date", "format": "date_hour_minute"},
                    "latitude": {"type": "float"},
                    "longitude": {"type": "float"},
                    #Again can add other fields
                }
            }
        }
        requests.put(f"{cls.es_url}/{cls.index_name}", json=settings, auth=cls.auth, verify=False)

    def test_document_operations(self):
        # Create a new document
        record = {
            "station": "Docklands",
            "current_date_time": "2024-05-03T14:00",
            "latitude": -37.8,
            "longitude": 145.0
        }
        create_response = requests.post(f"{self.es_url}/{self.index_name}/_doc", json=record, auth=self.auth, verify=False)
        print("Create Document Response:", create_response)
        self.assertEqual(create_response.status_code, 201)
        self.assertIn('result', create_response.json())
        self.assertEqual(create_response.json()['result'], 'created')
        
        # Store the document ID
        TestMelbourneWeatherOperations.doc_id = create_response.json()['_id']
        
        # Retrieve the document
        get_response = requests.get(f"{self.es_url}/{self.index_name}/_doc/{TestMelbourneWeatherOperations.doc_id}", auth=self.auth, verify=False)
        print("Retrieve Document Response", get_response)
        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(get_response.json()['_source']['station'], 'Docklands')
        
        # Delete the document #Can be commented out to see the doc live in ES
        delete_response = requests.delete(f"{self.es_url}/{self.index_name}/_doc/{TestMelbourneWeatherOperations.doc_id}", auth=self.auth, verify=False)
        print("Delete Document Response:", delete_response)
        self.assertEqual(delete_response.status_code, 200)
        self.assertEqual(delete_response.json()['result'], 'deleted')
        
        #Checking for non-existent id. Therefore implementing a test fail case.
        non_existent_id = '12345678-1234-1234-1234-123456789abc'
        response = requests.get(f"{self.es_url}/{self.index_name}/_doc/{non_existent_id}", auth=self.auth, verify=False)
        print(f"Retrieve Non-existent Document Response: {response.status_code} - {response.text}")
        self.assertEqual(response.status_code, 404, f"Expected a 404 status for non-existent document but got {response.status_code}")

if __name__ == '__main__':
    unittest.main()
