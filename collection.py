import sqlite3
from pprint import pprint

conn = sqlite3.connect('collection.anki2')

c = conn.cursor()

'''
dids = [
    1581278022264, # "新标准日本语初级(假名到解释)"
    1581278047538, # "新标准日本语初级(解释到假名)" 
    1582222331067, # "新标准日本语中级(假名到解释)"
    1582222406651, # "新标准日本语中级(解释到假名)"
    1582222636179, # "新标准日本语高级(假名到解释)"
    1582222618769, # "新标准日本语高级(解释到假名)"
]
'''

dids = [1598078013277, # 日语(假名到解释)-初级
]

for did in dids:
    c.execute('''
        SELECT c.*, CAST(n.sfld AS INTEGER), n.flds
        FROM cards c, notes n 
        WHERE c.nid == n.id 
            AND n.sfld != ""
            AND c.did == ?
        ORDER by CAST(n.sfld AS INTEGER)
    ''', (did,)
    )

    all = c.fetchall()
    print('[%s] len(all): %s' % (did, len(all)))

    with open('n5.js', 'w', encoding='utf-8') as fo:
        fo.write('var my_data = [\n')
        for entry in all:
            tmp = entry[-1].split('\x1f')
            #pprint(tmp)
            fo.write('[')
            for i in range(7):
                if i == 0 or i == 5:
                    fo.write(str(int(tmp[i])))
                elif i == 6:
                    fo.write('"'+tmp[i][7:-1]+'"')
                else:
                    fo.write('"'+tmp[i]+'"')
                if i < 6:
                    fo.write(',')
            fo.write('],\n')
            #break
        fo.write('];\n')
        
conn.commit()
conn.close()