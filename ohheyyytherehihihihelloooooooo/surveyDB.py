from google.appengine.ext import db

class Survey(db.Model):
    question = db.StringProperty()
    answerOne = db.StringProperty()
    answerTwo = db.StringProperty()
    answerThree = db.StringProperty()
    choice = db.StringProperty()
    which_user = db.UserProperty()
