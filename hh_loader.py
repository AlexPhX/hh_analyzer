import json
import datetime
import requests
from threads_downloader import start_dl_threads
from collections import Counter


def get_info_from_hh(params, pages, out_type):
    """
    :param params: Словарь вида  {"text": "KeyWord", "area": a, "period": p}
                    KeyWord - ключевое слово по которому будет осуществляться поиск
                    a - область по которой будет осуществляться поиск
                        (a = 1 - Москва)
                        (a = 2 - Санкт-Петербург)
                        ID других городов можно получить отправив GET запрос на
                        https://api.hh.ru/suggests/areas?text="Уфа"
                    p - перидод в днях за который будет собрана информация
                    Возможно использование других параметров:
                    https://github.com/hhru/api/blob/master/docs/vacancies.md#search

    :param pages: Количество страниц для сбора информации (0 - все страницы)
    :param out_type: Словарь вида {"urls": n1, "skills": n2, "vacs": n3}
                    В случае если n1, n2, n3 == 0 информация о ссылках,
                    навыках, вакансиях не будет включена в возвращаемый json.
    :return: json вида
            {"request_info" : информация о запросе
             "skills" : набор уникальных навыков с частотами
             "urls" : список обработанных ссылок
             "vacs" : информация о вакансиях}
    """
    params["page"] = 0
    urls = []
    resp = requests.get("https://api.hh.ru/vacancies", params=params)
    if resp.status_code == requests.codes.ok:
        js_out = json.loads(resp.text)
        if pages == 0:
            pages = int(js_out["pages"])
    else:
        print("Status code: " + str(resp.status_code))
        exit(-1)
    request_info = {"date": str(datetime.date.today()),
                    "url": resp.url,
                    "found": js_out["found"]}
    for p in range(pages):
        params["page"] = p
        js_out = json.loads(requests.get("https://api.hh.ru/vacancies",
                                         params=params).text)
        for it in js_out["items"]:
            urls.append(it["url"])
    vacs = []
    skills = Counter()
    start_dl_threads(urls, 10, vacs)
    for v in vacs:
        for i in v["key_skills"]:
            skills[i["name"].lower()] += 1
    js_out = {"request_info": request_info,
              "skills": skills if out_type["skills"] != 0 else None,
              "urls": urls if out_type["urls"] != 0 else None,
              "vacs": vacs if out_type["vacs"] != 0 else None
              }
    return js_out
