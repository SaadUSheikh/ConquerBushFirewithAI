import unittest
from elasticsearch8 import Elasticsearch


#To check if routes are working fine, and we are able to use get,delete,create etc methods.
class TestElasticsearchOperations(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Connect to the local Elasticsearch server
        cls.es = Elasticsearch(
            ['https://127.0.0.1:9200'],
            basic_auth=('elastic', 'password_goes_here'), 
            verify_certs=False
        )
        # Ensure the index does not exist
        cls.es.indices.delete(index='melbourne_weather_test', ignore=[400, 404])

        # Create a new index with mappings
        cls.es.indices.create(index='melbourne_weather_test', body={
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
                    # Can add other fields, for now we have just used four.
                }
            }
        })

    '''We can uncomment some function here, to check the process within Elasticsearch, here we are deleting the document plus the indices 
    after it performs its operations'''
    @classmethod
    def tearDownClass(cls):
        # Delete the index after tests
        cls.es.indices.delete(index='melbourne_weather_test', ignore=[400, 404])

    def test_document_operations(self):
        # Test adding a document
        doc = {
            "station": "Test Station",
            "current_date_time": "2024-05-03T14:00",
            "latitude": -37.8,
            "longitude": 145.0
        }
        response = self.es.index(index="melbourne_weather_test", id=1, body=doc)
        print("Create Document Response:", response)
        self.assertEqual(response['result'], 'created')

        # Test retrieving a document
        response = self.es.get(index="melbourne_weather_test", id=1)
        print("Retrieve Document Response:", response)
        self.assertEqual(response['_source']['station'], "Test Station")

        # Test deleting a document
        response = self.es.delete(index="melbourne_weather_test", id=1)
        print("Delete Document Response:", response)
        self.assertEqual(response['result'], 'deleted')

if __name__ == '__main__':
    unittest.main()
