import os
import sys
import requests
import time
import regex as re
import json
import ast
from pprint import pprint

katakana_chart = "ァアィイゥウェエォオカガキギクグケゲコゴサザシジスズセゼソゾタダチヂッツヅテデトドナニヌネノハバパヒビピフブプヘベペホボポマミムメモャヤュユョヨラリルレロヮワヰヱヲンヴヵヶヽヾ"
hiragana_chart = "ぁあぃいぅうぇえぉおかがきぎくぐけげこごさざしじすずせぜそぞただちぢっつづてでとどなにぬねのはばぱひびぴふぶぷへべぺほぼぽまみむめもゃやゅゆょよらりるれろゎわゐゑをんゔゕゖゝゞ"
hir2kat = str.maketrans(hiragana_chart, katakana_chart)
kat2hir = str.maketrans(katakana_chart, hiragana_chart)

re_row = re.compile(r'<tr id="word_\d+">(.*?)</tr>', flags=re.S | re.I)
re_cell = re.compile(r'<td class="katsuyo[^>]+>(.*?)</td>', flags=re.S | re.I)
re_a_tag = re.compile(r"<a[^>]+>.*?</a>", flags=re.S | re.I)
re_head_space = re.compile(r"^\s+<", flags=re.S | re.I | re.M)
re_tag = re.compile(r"<[^>]+?>", flags=re.S | re.I)

re_moji = re.compile(r'"accent":"(.*?)"', flags=re.S | re.I)

re_empty_ojad = re.compile(r"search_result_message", flags=re.S | re.I)
re_empty_hjenglish = re.compile(r"没有找到你查的单词结果", flags=re.S | re.I)


def down_section(textbook, n):
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


def down_book(textbook=7, cnt=32):
    for i in range(cnt):
        down_section(textbook, str(i + 1))


def down_word_ojad(word, n):
    n = str(n)
    fn = "accent/W" + n + ".html"
    if os.path.isfile(fn):
        print("%s exists" % fn)
        return

    url = (
        "http://www.gavo.t.u-tokyo.ac.jp/ojad/search/index/display:print"
        + "/sortprefix:accent/narabi1:kata_asc/narabi2:accent_desc/narabi3:mola_asc/yure:invisible/curve:invisible/details:invisible/limit:100/word:"
        + word
    )
    while True:
        try:
            r = requests.get(url, timeout=30)
            break
        except Exception:
            print("wait...")
            time.sleep(3)
    with open(fn, "wb") as f:
        if not re_empty_ojad.search(r.text):
            f.write(r.content)


def down_word_hjenglish(word, n):
    n = str(n)
    fn = "accent/W" + n + ".html"
    if os.path.isfile(fn):
        print("%s exists" % fn)
        return

    url = "https://dict.hjenglish.com/jp/jc/" + word
    while True:
        try:
            r = requests.get(url, timeout=30)
            break
        except Exception:
            print("wait...")
            time.sleep(3)
    with open(fn, "wb") as f:
        if not re_empty_hjenglish.search(r.text):
            f.write(r.content)


def down_word_moji(word, n):
    n = str(n)
    fn = "accent/W" + n + ".html"
    if os.path.isfile(fn):
        print("%s exists" % fn)
        return

    url = "https://api.mojidict.com/parse/functions/search_v3"
    headers = {
        "cache-control": "no-cache",
        "content-type": "application/json;charset=UTF-8",
        "pragma": "no-cache",
    }
    payload = {
        "searchText": word,
        "needWords": True,
        "langEnv": "zh-CN_ja",
        "_ApplicationId": "E62VyFVLMiW7kvbtVq3p",
    }
    while True:
        try:
            r = requests.post(
                url, headers=headers, data=json.dumps(payload), timeout=30
            )
            break
        except Exception:
            print("wait...")
            time.sleep(3)
    with open(fn, "wb") as f:
        if not re_empty_hjenglish.search(r.text):
            f.write(r.content)


def down_missing(site):
    with open("missing.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    print("len(data): %s" % len(data.items()))
    for word, n in data.items():
        print(word, n)
        if site == "ojad":
            down_word_ojad(word, n)
        elif site == "hjenglish":
            down_word_hjenglish(word, n)
        elif site == "moji":
            down_word_moji(word, n)


def get_word(el):
    word = re_tag.sub("", el)
    return word.strip()


def parse(data, html, n):
    rows = re_row.findall(html)
    # print("[%s] len(rows): %s" % (n, len(rows)))
    for row in rows:
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
    if len(rows) == 0:
        try:
            moji = json.loads(html)
            if (
                "result" in moji
                and "originalSearchText" in moji["result"]
                and "words" in moji["result"]
            ):
                word = moji["result"]["originalSearchText"].strip()
                for item in moji["result"]["words"]:
                    if "accent" in item and item["accent"]:
                        data[word] = {
                            10000
                            + n: "<p>"
                            + word
                            + '<span class="accent">'
                            + item["accent"]
                            + "</span></p>"
                        }
        except Exception as e:
            print("error: moji, ", e)
            pass


def parse_book(book="n5n4", cnt=48):
    data = {}
    for n in range(cnt):
        fn = "accent." + book + "/L" + str(n + 1) + ".html"
        with open(fn, "r", encoding="utf-8") as f:
            html = f.read()
            parse(data, html, n + 1)
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, separators=(",", ":"))


def parse_missing():
    with open("n5n4_more.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    print("len(54m): %s" % len(data.items()))
    with open("missing.json", "r", encoding="utf-8") as f:
        missing = json.load(f)
    print("len(missing): %s" % len(missing.items()))
    cnt = 0
    for word, n in missing.items():
        fn = "accent/W" + str(n) + ".html"
        if os.path.getsize(fn) == 0:
            continue
        with open(fn, "r", encoding="utf-8") as f:
            html = f.read()
        parse(data, html, 10000 + n)
        if (
            word in data
            or word.translate(kat2hir) in data
            or (word + "な") in data
            or (word.translate(kat2hir) + "な") in data
        ):
            cnt += 1
        else:
            print("Error: %s, %s" % (word, n))
    print("%s items added" % cnt)
    print("len(data): %s" % len(data.items()))
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, separators=(",", ":"))


def check_word(word, dict):
    if word in dict:
        return dict[word]
    elif (word + "な") in dict:
        dict[(word + "な")]["diff"] = True
        return dict[(word + "な")]
    elif word.translate(kat2hir) in dict:
        dict[word.translate(kat2hir)]["diff"] = True
        return dict[word.translate(kat2hir)]
    elif (word.translate(kat2hir) + "な") in dict:
        dict[word.translate(kat2hir) + "な"]["diff"] = True
        return dict[(word.translate(kat2hir) + "な")]
    else:
        return None


def check():
    data = {}
    data_missing = {}
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
    with open("n5n4_more.json", "r", encoding="utf-8") as f:
        n5n4_more = json.load(f)
    cnt_all = 0
    cnt_ok54 = 0
    cnt_ok32 = 0
    cnt_ok54m = 0
    cnt_missing = 0
    for word in words:
        cnt_all += 1
        r = check_word(word[1], n5n4)
        if r:
            data[word[1]] = r
            cnt_ok54 += 1
            continue
        r = check_word(word[1], n3n2)
        if r:
            data[word[1]] = r
            cnt_ok32 += 1
            continue
        r = check_word(word[1], n5n4_more)
        if r:
            data[word[1]] = r
            cnt_ok54m += 1
            continue
        data_missing[word[1]] = word[0]
        cnt_missing += 1
    print("cnt_all: %s" % cnt_all)
    print("cnt_ok54: %s" % cnt_ok54)
    print("cnt_ok32: %s" % cnt_ok32)
    print("cnt_ok54m: %s" % cnt_ok54m)
    print("cnt_missing: %s" % cnt_missing)
    print("len(data_missing): %s" % len(data_missing.items()))
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, separators=(",", ":"))
    if cnt_missing > 0:
        with open("missing.json", "w", encoding="utf-8") as f:
            json.dump(data_missing, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    # down_book()
    # parse_book()
    check()
    # down_missing("moji")
    # parse_missing()
