from google.appengine.ext import db

class FrontPage(db.Model):
    name = db.StringProperty()

    q1 = db.StringProperty()
    q1a1 = db.StringProperty()
    q1a2 = db.StringProperty()
    q1a3 = db.StringProperty()

    q2 = db.StringProperty()
    q2a1 = db.StringProperty()
    q2a2 = db.StringProperty()
    q2a3 = db.StringProperty()

    q3 = db.StringProperty()
    q3a1 = db.StringProperty()
    q3a2 = db.StringProperty()
    q3a3 = db.StringProperty()

    submit = db.StringProperty()
    results = db.StringProperty()

    choice = db.StringProperty()
    which_user = db.UserProperty()
