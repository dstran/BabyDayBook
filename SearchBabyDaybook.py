import sqlite3
from flask import Flask, g
from ChartItem import *

app = Flask(__name__)

class SearchBabyDaybook(object):
    def __init__(self, db):
        self.db = db

    def request_has_connection(self):
        return hasattr(g, 'dbconn')

    def execute(self, query, args):
        cur = self.get_db().execute(query, args)
        rv = cur.fetchall()
        print "len=", len(rv)
        cur.close()
        return rv

    def get_db(self):
        try:
            if not self.request_has_connection():
                print self.db
                g.dbconn = sqlite3.connect(self.db)
                g.dbconn.row_factory = sqlite3.Row
        except sqlite3.Error, e:
            print "Error %s:" % e.args[0]

        return g.dbconn

    @app.teardown_request
    def teardown_request(self, exception):
        if not self.request_has_connection():
            conn = self.get_db()
            conn.close()

    def query_db(self, text):
        #print text
        l = []
        l.append("select type, start_millis, end_millis, notes, volume, temperature, pee, poo, hair_wash, groups.daily_action_type, groups.title from daily_actions left outer join groups on daily_actions.group_uid = groups.uid where daily_actions.type like '%")
        l.append(text)
        l.append("%' or daily_actions.notes like '%")
        l.append(text)
        l.append("%' or groups.daily_action_type like '%")
        l.append(text)
        l.append("%' or groups.title like '%")
        l.append(text)
        l.append("%'")
        query = "".join(l)
        #print query
        rv = self.execute(query, '')
        return rv


    def prepare_chart(self):
        l = []
        l.append("select strftime('%W', start_millis / 1000, 'unixepoch') as week_number,")
        l.append("max(date(start_millis / 1000, 'unixepoch', 'weekday 0', '-7 day')) as week_start,")
        l.append("max(date(start_millis / 1000, 'unixepoch', 'weekday 0', '-1 day')) as week_end,")
        l.append("case cast (strftime('%w', start_millis / 1000, 'unixepoch') as integer)")
        l.append("when 0 then 'Sunday'")
        l.append("when 1 then 'Monday'")
        l.append("when 2 then 'Tuesday'")
        l.append("when 3 then 'Wednesday'")
        l.append("when 4 then 'Thursday'")
        l.append("when 5 then 'Friday'")
        l.append("else 'Saturday' end as day_of_week")
        l.append(",strftime('%Y-%m-%d %H:%M:%S', start_millis / 1000, 'unixepoch', 'localtime') as date_time,")
        l.append("type, start_millis, end_millis, notes, volume, temperature, pee, poo, hair_wash, ")
        l.append("groups.daily_action_type || '-' || groups.title as title ")
        l.append("from daily_actions left outer join groups on daily_actions.group_uid = groups.uid  group by start_millis")
        query = "".join(l)

        rv = self.execute(query, '')
        query_items = []
        for row in rv:
            item = QueryItem(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10],
                             row[11], row[12], row[13], row[14]);
            query_items.append(item)


        group = {}
        for q in query_items:
            bottle_vol = 0
            pump_vol = 0
            nap_dur = 0
            breastfeeding_dur = 0
            nighttime_dur = 0
            if q.type == 'bottle':
                bottle_vol = q.volume
            if q.type == 'pump':
                pump_vol = q.volume
            if q.type == 'breastfeeding':
                breastfeeding_dur = (q.end_millis - q.start_millis)/1000
            if q.title == 'sleeping-Nap':
                if q.end_millis > 0:
                    nap_dur = (q.end_millis - q.start_millis)/1000
            if q.title == 'sleeping-Nighttime':
                if q.end_millis > 0:
                    nighttime_dur = (q.end_millis - q.start_millis)/1000

            if q.week_number not in group:
                group[q.week_number] = ChartItem(q.start_millis, q.week_number, breastfeeding_dur, bottle_vol, pump_vol, q.pee, q.poo,
                                                 nap_dur, nighttime_dur)
            else: # Has key
                if group[q.week_number].start_millis == 0:
                    group[q.week_number].start_millis = q.start_millis
                group[q.week_number].breastfeeding_dur_sec += breastfeeding_dur
                group[q.week_number].bottle_ml += bottle_vol
                group[q.week_number].pump_ml += pump_vol
                group[q.week_number].pee_ct += q.pee
                group[q.week_number].poo_ct += q.poo
                group[q.week_number].nap_dur_sec += nap_dur
                group[q.week_number].nighttime_dur_sec += nighttime_dur

        #for g in group.values():
        #   print 'week_number: ', g.week_number, 'breastfeeding_dur: ', g.breastfeeding_dur_sec, 'pee_ct: ', g.pee_ct

        return group

