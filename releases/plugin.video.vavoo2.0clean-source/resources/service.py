# -*- coding: utf-8 -*-

import os, xbmc, time
from datetime import datetime, timedelta
from vavoo import utils, sql
from vavoo.epg import service as epg

datapath = utils.addonprofile
temppath = utils.cachepath
con = utils.con

def add_tables():
    cur = con.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS epg ( "id" INTEGER PRIMARY KEY AUTOINCREMENT, "cid" TEXT, "start" INTEGER, "end" INTEGER, "title" TEXT, "desc" TEXT, "lang" TEXT)')
    cur.execute('CREATE TABLE IF NOT EXISTS epgs ( "id" INTEGER PRIMARY KEY AUTOINCREMENT, "rid" TEXT, "mid" TEXT, "mn" TEXT, "tid" TEXT, "tn" TEXT, "display" TEXT, "ol" TEXT, "ml" TEXT, "tl" TEXT)')
    cur.execute('CREATE TABLE IF NOT EXISTS settings ( "name" TEXT, "value" TEXT)')
    con.commit()
    return True

def check_epg_tables():
    sqldata = sql.epg
    cur = con.cursor()
    for row in sqldata:
        cur.execute('SELECT * FROM epgs WHERE rid="' + row[1] + '"')
        data = cur.fetchone()
        if not data:
            cur.execute('INSERT INTO epgs VALUES (?,?,?,?,?,?,?,?,?,?)', row)
    con.commit()
    return True

def check():
    if add_tables():
        if check_epg_tables():
            cur = con.cursor()
            cur.execute('SELECT * FROM settings WHERE name="timestamp"')
            data = cur.fetchone()
            if data:
                timestamp = int(time.time())
                epg_grab_days = int(utils.addon.getSetting("epg_grab_days"))
                if not timestamp > int(data['value'])+epg_grab_days*86400:
                    xbmc.log('RETURN', xbmc.LOGINFO)
                    return
            xbmc.log('SERVICE', xbmc.LOGINFO)
            epg.run_grabber()

check()
