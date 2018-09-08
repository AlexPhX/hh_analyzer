import re
import json
from collections import Counter
from hh_loader import get_info_from_hh
import matplotlib.pyplot as plt
import numpy as np

langs = ("", "Java", "JavaScript",
         "Python", "C#",
         "C++", "PHP", "1С")

for l in langs:
    par = {"text": "Программист " + l, "search_field": "name", "area": 2, "period": 30}
    o = {"skills": 0, "urls": 0, "vacs": 1}
    vacs = get_info_from_hh(par, 0, o)
    with open("keywords.json", "r") as rf:
        kw = json.load(rf)
    data = Counter()
    n = 0
    for v in vacs["vacs"]:
        n += 1
        s = v["description"]
        for item in kw:
            pattern = r"(?i)[^а-яА-Яa-zA-Z0-9_|^]%s[^а-яА-Яa-zA-Z0-9_|$]" % kw[item]
            try:
                if re.search(pattern, s):
                    data[item] += 1
            except re.error:
                print("Проблема с элементом: " + kw[item])
    print("По запросу: \"%s\"" % par["text"])
    print("обработано %s вакансий" % str(n))
    print(data.most_common())

    plt.rcdefaults()
    fig, ax = plt.subplots()

    skill = [i[0] for i in data.most_common(20)]
    y_pos = np.arange(len(skill))
    frequency = [data[s] for s in skill]
    error = np.random.rand(len(skill))

    ax.barh(y_pos, frequency, align='center', color='blue')
    ax.set_yticks(y_pos)
    ax.set_yticklabels(skill)
    ax.invert_yaxis()  # labels read top-to-bottom
    ax.set_xlabel("Частота")
    ax.set_title("Запрос: \"%s\"\nОбработано %d вакансии(й)" % (par["text"], n))

    plt.tight_layout()
    plt.savefig("figures/" + par["text"] + ".png")