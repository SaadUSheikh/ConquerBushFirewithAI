from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
from elasticsearch8 import Elasticsearch
from datetime import datetime, timedelta
import logging
import json
import os
import pytz
import base64


logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

# Read Elasticsearch configuration from environment variables
es_host = os.getenv('ES_HOST', 'elasticsearch-master.elastic.svc.cluster.local')
es_port = os.getenv('ES_PORT','9200')
es_username = os.getenv('ES_USERNAME', 'elastic')
es_password = os.getenv('ES_PASSWORD', 'password_goes_here')

# try:
#     if es_password_encoded:
#         es_password = base64.b64decode(es_password_encoded).decode('utf-8')
#     else:
#         es_password = 'password_goes_here'
# except Exception as e:
#     print(f"Error decoding ES_PASSWORD: {e}")
#     es_password = 'password_goes_here' 

def parse_int(value):
    try:
        return int(value)
    except ValueError:
        return None  

def parse_float(value):
    try:
        return float(value)
    except ValueError:
        return None 
    
def parse_time(time_str_o):
    # Check if the time is "-" or empty
    if time_str_o in {"-", ""}:
        return None  
    try:
        # Parse time
        time_obj = datetime.strptime(time_str_o, '%I:%M%p')
        # Format to 24-hour time without date
        return time_obj.strftime('%H:%M')
    except ValueError as e:
        app.logger.error(f"Time parsing error: {e} for time_str: {time_str_o}")
        return None
    

# Define Melbourne timezone
melbourne_tz = pytz.timezone('Australia/Melbourne')

station_coordinates = {
        "Melbourne (Olympic Park)": {"lat": -37.8, "lon": 145.0},
        "Melbourne Airport": {"lat": -37.7, "lon": 144.8},
        "Avalon": {"lat": -38.0, "lon": 144.5},
        "Cerberus": {"lat": -38.4, "lon": 145.2},
        "Coldstream": {"lat": -37.7, "lon": 145.4},
        "Essendon Airport": {"lat": -37.7, "lon": 144.9},
        "Fawkner Beacon": {"lat": -37.9, "lon": 144.9},
        "Ferny Creek": {"lat": -37.9, "lon": 145.3},
        "Frankston (Ballam Park)": {"lat": -38.2, "lon": 145.2},
        "Frankston Beach": {"lat": -38.1, "lon": 145.1},
        "Geelong Racecourse": {"lat": -38.2, "lon": 144.4},
        "Laverton": {"lat": -37.9, "lon": 144.8},
        "Moorabbin Airport": {"lat": -38.0, "lon": 145.1},
        "Point Cook": {"lat": -37.9, "lon": 144.8},
        "Point Wilson": {"lat": -38.1, "lon": 144.5},
        "Rhyll": {"lat": -38.5, "lon": 145.3},
        "Scoresby": {"lat": -37.9, "lon": 145.3},
        "Sheoaks": {"lat": -37.9, "lon": 144.1},
        "South Channel Island": {"lat": -38.3, "lon": 144.8},
        "St Kilda Harbour RMYS": {"lat": -37.9, "lon": 145.0},
        "Viewbank": {"lat": -37.7, "lon": 145.1}
        
    }

def get_latitude(station_name):
    """Returns the latitude of the given station name."""
    return station_coordinates.get(station_name, {}).get("lat")

def get_longitude(station_name):
    """Returns the longitude of the given station name."""
    return station_coordinates.get(station_name, {}).get("lon")

def parse_time_UTC(melbourne_time_str, melbourne_date_str):
    # Check for empty or special values
    if melbourne_time_str in {"-", ""}:
            return None
    
    try:    
        # Parse Melbourne date and time string into a datetime object
        melbourne_datetime_str = f"{melbourne_date_str} {melbourne_time_str}"
        melbourne_datetime = datetime.strptime(melbourne_datetime_str, '%Y-%m-%d %I:%M%p')

        # Localize the datetime object to Melbourne timezone
        melbourne_datetime = melbourne_tz.localize(melbourne_datetime)

        # Convert to UTC time
        utc_datetime = melbourne_datetime.astimezone(pytz.utc)

        # Return the datetime in ISO 8601 format
        return utc_datetime.strftime('%Y-%m-%dT%H:%M')

    except ValueError:
        return None


@app.route('/fetch-bom-data', methods=['GET'])
def fetch_weather_data():
    # Initialize Elasticsearch client
    client = Elasticsearch(
        [f"https://{es_host}:{es_port}"],
        verify_certs=False,
        basic_auth=(es_username, es_password)
    )
    month_to_digit = {
    'January': '01',
    'February': '02',
    'March': '03',
    'April': '04',
    'May': '05',
    'June': '06',
    'July': '07',
    'August': '08',
    'September': '09',
    'October': '10',
    'November': '11',
    'December': '12'
}   

    try:
        app.logger.info("Attempting to fetch weather data")
        url = "http://reg.bom.gov.au/vic/observations/melbourne.shtml"
        response = requests.get(url)
        
        # Check for non-successful status codes
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')
        issued_info = soup.find('div', id='content').find("p").text.strip().split()
        date = ""
        if issued_info:
            date = issued_info[8] + "-" + month_to_digit[issued_info[7]] + "-" + issued_info[6]
        else:
            print("Issued information not found on the page.")

        observation_table = soup.find('table', id='tMELBOURNE')
        if observation_table:
            data = []
            rows = observation_table.find_all('tr')[1:]  # Skip header row
            app.logger.info("Successfully fetched and parsed weather data, now indexing.")
            for row in rows:
                name =  row.find('th')
                cells = row.find_all('td')
                if not cells:
                    app.logger.warning("No cells found in row, skipping.")
                    continue
                time_str = cells[0].text.strip()[3:]       
                # Log the raw time_str
                app.logger.info(f"Raw time_str: {time_str}")
            
                if cells:
                    row_data = {
                        "station": name.text.strip(),
                        "current_date_time": parse_time_UTC(time_str,date),
                        "latitude": get_latitude(name.text.strip()),
                        "longitude": get_longitude(name.text.strip()),
                        "temp": parse_float(cells[1].text.strip()),
                        "app_temp": parse_float(cells[2].text.strip()),
                        "dew_point": parse_float(cells[3].text.strip()),
                        "rel_hum": parse_float(cells[4].text.strip()),
                        "delta_t": parse_float(cells[5].text.strip()),
                        "wind_dir": cells[6].text.strip(),
                        "wind_spd": parse_int(cells[7].text.strip()),
                        "wind_gust": parse_int(cells[8].text.strip()),
                        "wind_spd_kts": parse_int(cells[9].text.strip()),
                        "wind_gust_kts": parse_int(cells[10].text.strip()),
                        "press_msl": parse_float(cells[11].text.strip()),
                        "rain": parse_float(cells[12].text.strip()),
                        "low_temp": parse_float(cells[13].text.strip()[:-7]),
                        "low_time": parse_time(cells[13].text.strip()[-7:]),
                        "high_temp": parse_float(cells[14].text.strip()[:-7]),
                        "high_time": parse_time(cells[14].text.strip()[-7:]),
                        "high_wind_gust_dir": cells[15].text.strip(),
                        "high_wind_gust_kmh": parse_int(cells[16].text.strip()[:-7]),
                        "high_wind_gust_kts": parse_int(cells[17].text.strip()[:-7]),
                        "high_wind_gust_time": parse_time(cells[17].text.strip()[-7:])
                    }
                    data.append(row_data)
                    res = client.index(index="melbourne_weather", body=row_data)
                    app.logger.info(f"Indexed data: {res}")
            pretty_json = json.dumps(data, indent=4)
            return app.response_class(pretty_json, content_type="application/json"), 200

        else:
            return jsonify({"error": "Observation table not found."}), 404
    except requests.HTTPError as http_err:
        # Specific HTTP error handling
        return jsonify({"error": "HTTP error occurred", "details": str(http_err)}), 500
    except Exception as err:
        # Generic error handling for any other exception
        return jsonify({"error": "An error occurred", "details": str(err)}), 500

if __name__ == "__main__":
    app.run(port=9090)  # The port number here should match the one set for service in Kubernetes
