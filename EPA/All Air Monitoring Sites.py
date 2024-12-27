import requests
import json

# Set the URL and API key
url = "https://gateway.api.epa.vic.gov.au/environmentMonitoring/v1/sites?environmentalSegment=air"
#api_key = "4fe5eadc43624b2882e5b62e01a1d1c7"
api_key = "4fe5eadc43624b2882e5b62e01a1d1c7"


# Set the headers including a User-Agent
headers = {
    "Cache-Control": "no-cache",
    "X-API-Key": api_key,
    "User-Agent": "MyApp/1.0"  # Customize the User-Agent to reflect your app or personal use
}

# Send the GET request
response = requests.get(url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    # Print the response data
    print("Response data:", response.json())
    
    data = response.json()
    
    # Specify the path where the file will be saved
    file_path = r'C:/Users/Owner/Downloads/output_allairmonitoringsites.json'
    
    # Write the JSON data to a file
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)
    
    print(f"Data saved to {file_path}")
else:
    # Print an error message if the request failed
    print("Failed to retrieve data. Status code:", response.status_code)
    
