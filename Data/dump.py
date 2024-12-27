import json

def beautify_json(input_file_path, output_file_path):
    try:
        with open(input_file_path, 'r') as file:
            data = json.load(file)
        
        with open(output_file_path, 'w') as file:
            json.dump(data, file, indent=4)  # Set indent level to 4 spaces
        print("JSON data has been beautified and saved.")
    except Exception as e:
        print(f"An error occurred: {e}")


input_path = '/Users/pranavpai/Code/Cloud_A2/team_4_90024_clustercloud/data/Trees_External_Data/bird-survey-results-for-areas-in-the-city-of-melbourne-february-and-march-2018.json'
output_path = '/Users/pranavpai/Code/Cloud_A2/team_4_90024_clustercloud/data/Trees_External_Data/Birds_Data.json'

beautify_json(input_path, output_path)
