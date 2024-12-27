import json
from elasticsearch8 import Elasticsearch, helpers

def load_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def bulk_index(es_client, index_name, data):
    actions = [
        {
            "_index": index_name,
            "_source": doc
        }
        for doc in data
    ]
    helpers.bulk(es_client, actions)

def main():
    es_client = Elasticsearch(
        ['https://127.0.0.1:9200'],
        basic_auth=('elastic', 'password_goes_here'),
        verify_certs=False
    )
    
    file_path = '/Users/pranavpai/Code/Cloud_A2/team_4_90024_clustercloud/data/Population_density_data/population_greater_melbourne.json'
    data = load_data(file_path)
    index_name = 'population_density_sudo'
    
    bulk_index(es_client, index_name, data)
    print("Data indexed successfully.")

if __name__ == "__main__":
    main()

