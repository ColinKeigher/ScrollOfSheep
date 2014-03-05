import os
import sqlite3
from time import time

# Uses this to track everything
class tracking():
    def __init__(s):
        s.dbfile = 'storage.db'
        create_db = s._db_exist()
        s.con = sqlite3.connect(s.dbfile)
        s.time_check = 10 # Minutes between seeing the same device show up again
        if create_db != True:
            s._db_create()

    def _db_create(s):
        q = 'CREATE TABLE tracking (type TEXT, bssid TEXT, device TEXT, ssid TEXT, datetime INT)'
        s._db_execute(q)

    def _db_execute(s, query, strings=None, return_data=False):
        with s.con:
            cur = s.con.cursor()
            if strings != None:
                cur.execute(query, strings) # Strings must be a tuple
            else:
                cur.execute(query)
            if return_data:
                return cur.fetchall()
            else:
                s.con.commit()

    def _db_exist(s):
        return os.path.isfile(s.dbfile)

    def insert(s):
        q = 'INSERT INTO tracking (type, bssid, device, ssid, datetime) VALUES (?, ?, ?, ?, ?)'
        wtype, bssid, device, ssid, datetime = s.data['type'], s.data['bssid'], s.data['device'], s.data['ssid'], s.data['time']
        s._db_execute(query=q, strings=(wtype, bssid, device, ssid, datetime))

    # Returns t/f based on whether or not it has been recent since the AP was found
    def insert_recent(s):
        output = False
        q = 'SELECT * FROM tracking WHERE bssid = ? ORDER BY datetime DESC LIMIT 1'
        item = s._db_execute(query=q, strings=(s.data['bssid'],), return_data=True)
        if len(item) > 0:
            output = (time() - int(item[0][4])) > s.time_check
        return output