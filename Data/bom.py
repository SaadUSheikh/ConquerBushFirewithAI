import requests
from bs4 import BeautifulSoup
import json

jsons=[]

# URL of the webpage
url = "http://reg.bom.gov.au/vic/observations/melbourne.shtml"


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

# Send a GET request to the URL
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    issued_info = soup.find('div', id='content').find("p").text.strip().split()
    date = ""
    # Extract and print the text
    if issued_info:
        date = issued_info[8] + "-" + month_to_digit[issued_info[7]] + "-" + issued_info[6]
        print(date)
    else:
        print("Issued information not found on the page.")

    # Finding all links on the webpage
    links = soup.find_all('a')
    for link in links:
        href = link.get('href')
        if href.startswith("/products/IDV60901/IDV60901"):
            jsons.append((link.text.strip(),href[10:-6]))

    # Find the table containing observations
    observation_table = soup.find('table', id='tMELBOURNE')
    
    # Extract data from the table
    if observation_table:
        rows = []
        data = {"rows": rows}
        rows__ = observation_table.find_all('tr')
        for row in rows__:
            name = row.find('th')
            cells = row.find_all('td')
            if cells:
                row_data = {
                    "station": name.text.strip(),
                    "time": cells[0].text.strip(),
                    "temp": cells[1].text.strip(),
                    "app_temp": cells[2].text.strip(),
                    "dew_point": cells[3].text.strip(),
                    "rel_hum": cells[4].text.strip(),
                    "delta_t": cells[5].text.strip(),
                    "wind_dir": cells[6].text.strip(),
                    "wind_spd": cells[7].text.strip(),
                    "wind_gust": cells[8].text.strip(),
                    "wind_spd_kts": cells[9].text.strip(),
                    "wind_gust_kts": cells[10].text.strip(),
                    "press_msl": cells[11].text.strip(),
                    "rain": cells[12].text.strip(),
                    "low_temp": cells[13].text.strip()[:-7],
                    "low_time": cells[13].text.strip()[-7:],
                    "high_temp": cells[14].text.strip()[:-7],
                    "high_time": cells[14].text.strip()[-7:],
                    "high_wind_gust_dir": cells[15].text.strip(),
                    "high_wind_gust_kmh": cells[16].text.strip()[:-7],
                    "high_wind_gust_kts": cells[17].text.strip()[:-7],
                    "high_wind_gust_time" : cells[17].text.strip()[-7:]
                }
                rows.append(row_data)
        with open('./all.json', 'w') as f:
            json.dump(data, f, indent=4)
    else:
        print("Observation table not found.")
else:
    print("Failed to retrieve data. Status code:", response.status_code)




for j in jsons:
    url = "http://reg.bom.gov.au/fwo/" + j[1] + ".json"

    response = requests.get(url)


    if response.status_code == 200:
        json_data = response.json()
        with open( j[0] + '.json', 'w') as f:
            json.dump(json_data, f, indent=4)
    else:
        print("Failed to retrieve data. Status code:", response.status_code)