import json
import datetime
import requests
from threads_downloader import start_dl_threads
from collections import Counter

skills = Counter()
urls = []
vacs = []

pages = 1
params = {"text": "Java", "area": 2, "page": 0, "period": 7}
resp = requests.get("https://api.hh.ru/vacancies", params=params)
if resp.status_code == requests.codes.ok:
    js_out = json.loads(resp.text)
    if pages == 0:
        pages = int(js_out["pages"])
else:
    print("Status code: " + str(resp.status_code))
    exit(-1)
request_info = {"date": str(datetime.date.today()),
                "url": resp.url}
for p in range(pages):
    params["page"] = p
    js_out = json.loads(requests.get("https://api.hh.ru/vacancies",
                                     params=params).text)
    for it in js_out["items"]:
        vac_j = json.loads(requests.get(it["url"]).text)
        urls.append(it["url"])
start_dl_threads(urls, 5, vacs)
for v in vacs:
    for i in v["key_skills"]:
        skills[i["name"]] += 1
jsout = {"request_info" : request_info,
         "skills" : skills,
         "urls" : urls,
         "vacs" : vacs
        }
with open("data\data_" + str(datetime.date.today()) + ".json", "w") as f:
    json.dump(jsout, f, indent=4)
