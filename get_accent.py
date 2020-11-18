import os
import sys
import requests
import regex as re
import json


def down(n):
    n = str(n)
    fn = "accent/L" + n + ".html"
    if os.path.isfile(fn):
        print("%s exists" % fn)
        return

    url = (
        "http://www.gavo.t.u-tokyo.ac.jp/ojad/search/index/display:print/textbook:6/section:"
        + n
        + "-"
        + n
        + "/sortprefix:accent/narabi1:kata_asc/narabi2:accent_desc/narabi3:mola_asc/yure:invisible/curve:invisible/details:invisible/limit:100"
    )
    r = requests.get(url)
    with open(fn, "wb") as f:
        f.write(r.content)


def down_all():
    for i in range(48):
        down(str(i + 1))


def get_word(el):
    re_tag = re.compile(r"<[^>]+?>", flags=re.S | re.I)
    word = re_tag.sub("", el)
    return word.strip()


def parse(data, n):
    n = str(n)
    fn = "accent/L" + n + ".html"
    with open(fn, "r", encoding="utf-8") as f:
        html = f.read()
    re_row = re.compile(r'<tr id="word_\d+">(.*?)</tr>', flags=re.S | re.I)
    rows = re_row.findall(html)
    print("len(rows): %s" % len(rows))
    i = 0
    for row in rows:
        i += 1
        if i != 3:
            # continue
            pass
        # print(row)
        re_cell = re.compile(r'<td class="katsuyo[^>]+>(.*?)</td>', flags=re.S | re.I)
        cells = re_cell.findall(row)
        for cell in cells:
            cell = cell.strip()
            if not cell:
                continue
            re_a_tag = re.compile(r"<a[^>]+>.*?</a>", flags=re.S | re.I)
            cell = re_a_tag.sub("", cell)
            re_head_space = re.compile(r"^\s+<", flags=re.S | re.I | re.M)
            cell = re_head_space.sub("<", cell)
            # print("[" + cell + "]")
            word = get_word(cell)
            # print("[" + word + "]")
            data[word] = cell


def parse_all():
    data = {}
    for n in range(48):
        parse(data, n + 1)
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


parse_all()