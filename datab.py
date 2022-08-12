# -*- coding: utf-8 -*-
#!/usr/bin/env python3

# owner github: https://github.com/beautiful-white
# GPL-2.0 License
# 2022 © Beautiful-White

import json
import time
from fuzzywuzzy import fuzz
import os

class Base(object):

    db = {}

    last_backup = None

    debug = True
    
    def backup(self):
        if not os.path.exists("backups"):
            os.makedirs("backups")
        nm = fr".\backups\backup_{round(time.time())}.db"
        with open(nm, "w")as bk:
            bk.write(json.dumps(self.db, ensure_ascii=False))
            print("[!] Успешный бэкап базы данных!")
            self.last_backup = nm
            print(f"    {nm}")if self.debug else 1

    def load(self, name=""):
        if not name: return print("[!] Вы не ввели имя бэкапа")
        print(r"[!] Загрука бэкапа {0}...".format(name.replace(".db", '') + ".db"))
        try:
            with open(name.replace(".db") + ".db", "r", encoding="utf-8") as data:
                self.db = json.loads(data.read())
                return print("[!] Успешная загрузка бэкапа данных!")
        except:
            name = name.replace(".db", '') + ".db"
            with open(r".\backups\\"+(name.replace(r".\backups\\", '')), "r", encoding="utf-8") as data:
                    self.db = json.loads(data.read())
                    return print("[!] Успешная загрузка бэкапа данных!")
            try:
                with open(r".\backups\\"+(name.replace(".db", '') + ".db").replace(r".\backups\\", ''), "r", encoding="utf-8") as data:
                    self.db = json.loads(data.read())
                    print("[!] Успешная загрузка бэкапа данных!")
            except:
                return print('''[!] Бэкап с таким именем не найден в директории БД!''')

    def loadLast(self):
        if self.last_backup:
            try:
                with open(self.last_backup, "r", encoding="utf-8") as data:
                    self.db = json.loads(data.read())
                    print("[!] Успешная загрузка последнего бэкапа данных!")
            except:
                return print('''[!] Бэкап с таким именем не найден в директории БД!''')

    
    def print_percent(self, l):
        print("[!] На запрос было отвечено:")
        print(l)
        for i in l:
                print(f"{i[0]} - {i[1]}% совпадения")
        if l == [[]]:
            print("[!] Совпадений не найдено!") 

    def __init__(self):
        print("[!] База подключена, бэкап базы данных...")
        self.backup()

    def __call__(self, c_id, sent, ans=""):
        if type(self.db.get(c_id)) != dict:
            self.db[c_id] = dict()
        sent = sent.lower()
        sent = sent.split()
        #sent.sort()
        sent = "".join(sent)
        if not ans:
            qwe = []
            for i in self.db[c_id].keys():
                qwe.append([i, fuzz.ratio(i, sent)])
            qwe = list(filter(lambda x: x[1] >= 70, qwe))
            return qwe
            #for i in sent:
            #    qwe.append(list(filter(lambda x: x[1] >= 70, process.extract(i, list(self.db.keys())))))
            #self.print_percent(qwe)
        else:
            self.db[c_id][sent] = ans
            print(f'''[!] ДБ обновлена
    "{sent}" = "{ans}"''') if self.debug else 1

    
            
        
        







if __name__ == "__main__":
    print("База данных не является исполняемой часть проекта!")
    exit()
    
