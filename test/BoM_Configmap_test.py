import os
import yaml
import unittest
import requests
import base64
from requests.auth import HTTPBasicAuth
import logging

def read_config_yaml(config_file, key):
    """ Reads configuration values from a YAML file and handle missing keys. """
    try:
        with open(config_file, 'r') as file:
            config = yaml.safe_load(file)
            data_config = config.get('data', {})
            if key in data_config:
                return data_config[key]
            else:
                raise KeyError(f"Key {key} not found in the configuration.")
    except FileNotFoundError:
        raise FileNotFoundError(f"The configuration file {config_file} was not found.")
    except yaml.YAMLError as exc:
        raise RuntimeError(f"Error parsing YAML file: {exc}")

class TestElasticsearchConnection(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        config_path = '../backend/es-config.yaml'
        credentials_path = '../backend/es-credentials.yaml' 

        host = read_config_yaml(config_path, 'ES_HOST')
        port = read_config_yaml(config_path, 'ES_PORT')
        cls.es_url = f"https://127.0.0.1:{port}"
        
        # Read the credentials from the YAML file
        username = read_config_yaml(credentials_path, 'ES_USERNAME')
        encoded_password = read_config_yaml(credentials_path, 'ES_PASSWORD')
        password = base64.b64decode(encoded_password).decode('utf-8')
        
        cls.auth = HTTPBasicAuth(username, password)

    def test_es_connection(self):
        """ Test the connection to Elasticsearch and check for a JSON response. """
        response = requests.get(f"{self.es_url}", auth=self.auth, verify=False)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.json())
        
        logging.info("Response received: %s", response.json())
        print("JSON Response:", response.json())


if __name__ == '__main__':
    unittest.main()
