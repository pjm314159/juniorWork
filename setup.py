import os
from sqlite3 import connect
os.system("pyinstaller -i favicon.ico -w run.spec")
coon = connect("content.db")
cur = coon.cursor()
pl = ["syjszpc", 'xxmh88', "realPeople", "goddess"]
a = [cur.execute(f"CREATE TABLE IF not exists {u} (url TEXT,name TEXT);") for u in pl]
coon.commit()
cur.close()
coon.close()