import json

# Open the JSON file
with open('raw.json', 'r') as f:
    # Load the JSON data into a Python dictionary
    data = json.load(f)["features"]

# Now you can work with the 'data' dictionary
items = []
for d in data:
    item = d["properties"]
    item["geometry"] = d["geometry"]
    items.append(item)


with open("raw2.json", "w") as json_file:
    json.dump(items, json_file, indent=4)