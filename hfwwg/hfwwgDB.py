from google.appengine.ext import db

class Sighting(db.Model):
    name = db.StringProperty()
    email = db.StringProperty()
    date = db.StringProperty()
    time = db.StringProperty()
    location = db.StringProperty()
    fin_type = db.StringProperty()
    whale_type = db.StringProperty()
    blow_type = db.StringProperty()
    wave_type = db.StringProperty()
