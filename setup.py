from sqlite3 import connect
coon = connect("static/content.db")
cur = coon.cursor()
pl = ["syjszpc", 'xxmh88', "realPeople", "goddess","jm"]
a = [cur.execute(f"CREATE TABLE IF not exists {u} (url TEXT,name TEXT);") for u in pl]
coon.commit()
cur.close()
coon.close()