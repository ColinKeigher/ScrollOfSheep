# -*- coding: utf-8 -*-

import os
import sqlite3
import pickle
from time import time

# Uses this to track everything
class tracking():
    def __init__(s):
        s.dbfile = 'storage.db'
        create_db = s._db_exist()
        s.con = sqlite3.connect(s.dbfile)
        s.stats_types = [ 'ap', 'client', 'bt' ]
        s.stats_keys = [ 'type', 'bssid', 'device', 'ssid', 'time' ]
        s.time_check = 5 # Minutes between seeing the same device show up again
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

    def _stats(s):
        output = {}
        for data_type in s.stats_types:
            output[data_type] = s._stats_build(data_type)
        return output

    def _stats_build(s, dev_type):
        q = 'SELECT * FROM tracking WHERE type = ? ORDER BY datetime DESC LIMIT 10'
        items = s._db_execute(query=q, strings=(dev_type, ), return_data=True)
        return s._stats_clean(items)

    def _stats_clean(s, items):
        return [ s._stats_clean_item(x) for x in items if len(items) != 0 ]

    def _stats_clean_item(s, item):
        data = {}
        for x in xrange(0, len(s.stats_keys)):
            current = s.stats_keys[x]
            data[current] = item[x]
        return data

    def insert(s):
        q = 'INSERT INTO tracking (type, bssid, device, ssid, datetime) VALUES (?, ?, ?, ?, ?)'
        s._db_execute(query=q, strings=(s.data['type'], s.data['bssid'], s.data['device'], s.data['ssid'], s.data['time']))

    # Returns t/f based on whether or not it has been recent since the device was found
    def insertable(s):
        output = True
        q = 'SELECT * FROM tracking WHERE bssid = ? ORDER BY datetime DESC LIMIT 1'
        item = s._db_execute(query=q, strings=(s.data['bssid'],), return_data=True)
        if len(item) > 0:
            output = (time() - int(item[0][4])) < s.time_check
        return output

    # Really meant for checking for APs
    def new(s):
        q = 'SELECT * FROM tracking WHERE bssid = ? AND ssid = ? LIMIT 1'
        item = s._db_execute(query=q, strings=(s.data['bssid'], s.data['ssid']), return_data=True)
        return len(item) == 0

    # Building stats for the web interface
    def stats(s):
        return s._stats()

# Keep track of things for the web interface
class web_track():
    def __init__(s, data=None):
        s.data = data
        s.data_file = 'webtrack.dat'
        s._init()

    def _init(s):
        if s._pickle_exist():
            s._load()
        else:
            s.items = {}

    def _load(s):
        s.items = pickle.load(open(s.data_file, 'rb'))

    def _save(s):
        pickle.dump(s.items, open(s.data_file, 'wb'))

    def _pickle_exist(s):
        return os.path.isfile(s.data_file)

    def _update_now(s):
        s.items['last_update'] = time()
        s._save()

    def _update_last(s):
        return s.items['last_update']

    #def _update_stats(s):
    #    for 

    def item_data(s):
        if 'data' in s.items.keys():
            return s.items['data']
        else:
            return None

    def insert(s):
        s.items['data'] = s.data
        s._update_now()

    def clear(s):
        s.items['data'] = {}
        s._update_now()

    def overwrite(s, data):
        s.items['data'] = {}
        s.items['data'] = data
        s._update_now()

    def last(s):
        return s._update_last()