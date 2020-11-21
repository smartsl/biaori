import os
import sys
import requests
import regex as re
import json
import ast
from pprint import pprint

re_row = re.compile(r'<tr id="word_\d+">(.*?)</tr>', flags=re.S | re.I)
re_cell = re.compile(r'<td class="katsuyo[^>]+>(.*?)</td>', flags=re.S | re.I)
re_a_tag = re.compile(r"<a[^>]+>.*?</a>", flags=re.S | re.I)
re_head_space = re.compile(r"^\s+<", flags=re.S | re.I | re.M)
re_tag = re.compile(r"<[^>]+?>", flags=re.S | re.I)


def down(textbook, n):
    textbook = str(textbook)
    n = str(n)
    fn = "accent/L" + n + ".html"
    if os.path.isfile(fn):
        print("%s exists" % fn)
        return

    url = (
        "http://www.gavo.t.u-tokyo.ac.jp/ojad/search/index/display:print/textbook:"
        + textbook
        + "/section:"
        + n
        + "-"
        + n
        + "/sortprefix:accent/narabi1:kata_asc/narabi2:accent_desc/narabi3:mola_asc/yure:invisible/curve:invisible/details:invisible/limit:100"
    )
    r = requests.get(url)
    with open(fn, "wb") as f:
        f.write(r.content)


def down_all(textbook=7, cnt=32):
    for i in range(cnt):
        down(textbook, str(i + 1))


def get_word(el):
    word = re_tag.sub("", el)
    return word.strip()


def parse(data, html, n):
    rows = re_row.findall(html)
    print("[%s] len(rows): %s" % (n, len(rows)))
    i = 0
    for row in rows:
        i += 1
        if i != 3:
            # continue
            pass
        # print(row)
        cells = re_cell.findall(row)
        for cell in cells:
            cell = cell.strip()
            if not cell:
                continue
            cell = re_a_tag.sub("", cell)
            cell = re_head_space.sub("<", cell)
            # print("[" + cell + "]")
            word = get_word(cell)
            # print("[" + word + "]")
            if not word in data:
                data[word] = {}
            data[word][n] = cell


def parse_all(cnt=32):
    data = {}
    for n in range(cnt):
        fn = "accent/L" + str(n + 1) + ".html"
        with open(fn, "r", encoding="utf-8") as f:
            html = f.read()
            parse(data, html, n + 1)
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, separators=(",", ":"))


def check():
    data = {}
    words = []
    with open("n5n4.js", "r", encoding="utf-8") as f:
        while True:
            line = f.readline()
            if not line:
                break
            try:
                tmp = ast.literal_eval(line)
                words.append(tmp[0])
            except Exception:
                pass
    with open("n5n4.json", "r", encoding="utf-8") as f:
        n5n4 = json.load(f)
    with open("n3n2.json", "r", encoding="utf-8") as f:
        n3n2 = json.load(f)
    cnt_all = 0
    cnt_ok = 0
    cnt_ok32 = 0
    for word in words:
        if word[1] in n5n4:
            cnt_ok += 1
        elif word[1] in n3n2:
            data[word[1]] = n3n2[word[1]]
            print(word)
            pprint(n3n2[word[1]])
            cnt_ok32 += 1
    print(cnt_all)
    print(cnt_ok)
    print(cnt_ok32)
    with open("n5n4_more.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, separators=(",", ":"))


# down_all()
# parse_all()
check()