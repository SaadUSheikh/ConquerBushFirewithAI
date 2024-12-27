import json
from elasticsearch8 import Elasticsearch, helpers  # Ensure correct import
import logging  

def load_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    print("Loaded documents:", len(data))  
    return data


def save_failed_docs(failed_docs):
    with open('failed_docs.json', 'w') as file: 
        json.dump(failed_docs, file, indent=4)

def bulk_index(es_client, index_name, data):
    actions = [
        {
            "_index": index_name,
            "_source": {
                "geo_point_2d": doc["geo_point_2d"],
                "geo_shape": {
                    "type": doc["geo_shape"]["geometry"]["type"],  
                    "coordinates": doc["geo_shape"]["geometry"]["coordinates"]
                },
                "properties": doc.get("properties", {}),  
                "source": doc.get("source", ""),
                "shape_area": doc.get("shape_area", ""),
                "soil": doc.get("soil", ""),
                "sub_base": doc.get("sub_base", ""),
                "shape_len": doc.get("shape_len", "")
            }
        } for doc in data if 'geo_shape' in doc and 'geo_point_2d' in doc  
    ]

    # Attempt to index the documents in bulk and handle the response
    try:
        successes, errors = helpers.bulk(es_client, actions, index=index_name, raise_on_error=False)
        print(f"Indexed {successes} documents successfully.")
        if errors:
            print(f"Failed to index {errors} documents.")
            # Save or handle failed documents here
    except Exception as e:
        logging.error("An error occurred during bulk indexing: ", exc_info=True)


def main():
    logging.basicConfig(level=logging.INFO)
    es_client = Elasticsearch(
        ['https://127.0.0.1:9200'],
        basic_auth=('elastic', 'password_goes_here'),
        verify_certs=False
    )
    
    file_path = '/Users/pranavpai/Code/Cloud_A2/team_4_90024_clustercloud/data/Trees_External_Data/Beautified_JSON/Soil_Types_Urban.json'
    data = load_data(file_path)
    index_name = 'soil_ext_data'

    bulk_index(es_client, index_name, data)

if __name__ == "__main__":
    main()


