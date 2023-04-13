import requests
import json
from bs4 import BeautifulSoup

initialurl = "https://contentzone.eurocontrol.int/aircraftperformance/details.aspx?ICAO=A10"
res = requests.get(initialurl)

soup = BeautifulSoup(res.content, "html.parser")

codes = []

for s in str(soup.find(id="wsGroupDropDownList").prettify()).split("\n"):
    if s.strip().startswith("<"):
        continue
    else:
        if s.strip() == "":
            continue
        else:
            codes.append(s.strip())

output = {}

recat_abbr = {
        "Light": "L",
        "Lower Medium": "LM",
        "Upper Medium": "UM",
        "Lower Heavy": "LH",
        "Upper Heavy": "UH",
        "Super Heavy": "SH",
        "Special": "S",
        "No code": "--"
        }

for i, code in enumerate(codes):
    print(f"{i}/{len(codes)}")
    url = f"https://contentzone.eurocontrol.int/aircraftperformance/details.aspx?ICAO={code}"
    res = requests.get(url)

    if res.status_code != 200:
        continue

    soup = BeautifulSoup(res.content, "html.parser")

    apc = soup.find(id="MainContent_wsAPCLabel").text
    wtc = soup.find(id="MainContent_wsWTCLabel").text
    recat_raw = soup.find(id="MainContent_wsRecatEULabel").text
    recat = recat_abbr[recat_raw]
    name = soup.find(id="MainContent_wsAcftNameLabel").text
    
    output[code] = {"APC": apc, "WTC": wtc, "RECAT": recat, "Name": name}

with open("data.json", "w+") as f:
    f.write(json.dumps(output))
