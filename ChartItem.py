class ChartItem(object):
    def __init__(self, start_millis, week_number, breastfeeding_dur_sec, bottle_ml, pump_ml, pee_ct, poo_ct, nap_dur_sec,
                 nighttime_dur_sec):
        self.start_millis = start_millis
        self.week_number = week_number
        self.breastfeeding_dur_sec = breastfeeding_dur_sec
        self.bottle_ml = bottle_ml
        self.pump_ml = pump_ml
        self.pee_ct = pee_ct
        self.poo_ct = poo_ct
        self.nap_dur_sec = nap_dur_sec
        self.nighttime_dur_sec = nighttime_dur_sec


class QueryItem(object):
    def __init__(self, week_number, week_start, week_end, day_of_week, date_time, action_type, start_millis, end_millis, notes,
                 volume, temperature, pee, poo, hair_wash, title):
        self.week_number = week_number
        self.week_start = week_start
        self.week_end = week_end
        self.day_of_week = day_of_week
        self.date_time = date_time
        self.type = action_type
        self.start_millis = start_millis
        self.end_millis = end_millis
        self.notes = notes
        self.volume = volume
        self.temperature = temperature
        self.pee = pee
        self.poo = poo
        self.hair_wash = hair_wash
        self.title = title
