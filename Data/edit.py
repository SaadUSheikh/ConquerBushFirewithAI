import json

# Your JSON data
with open('abs_regional_population_sa2_2001_2021-4851612621186898305.json', 'r') as file:
    json_data = file.read()

# Parse the JSON
parsed_json = json.loads(json_data)



# Beautify the JSON

for i in parsed_json["features"]:
    for j in i["properties"].keys():
        if j.startswith("birth"):
            continue
        if j.startswith("overseas"):
            continue
        if j.startswith("internal"):
            continue
        if j.startswith("erp_change"):
            continue
        if j.startswith("natural"):
            continue
        if j.startswith("net"):
            continue
        if j.startswith("erp") and j[-1] != "1":
            continue
        if j.startswith("deaths"):
            continue
        i[j] = i["properties"][j]
    del i["properties"]
    del i["type"]





greater_json = []
parsed_json = parsed_json["features"]

for i in parsed_json:
    if i["gccsa_name_2016"] == "Greater Melbourne":
        greater_json.append(i)

with open('population_greater_melbourne.json', 'w') as file:
    file.write(json.dumps(greater_json, indent=4))