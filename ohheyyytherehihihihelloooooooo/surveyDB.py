from google.appengine.ext import db

class Survey(db.Model):
    question = db.StringProperty()
    answerOne = db.StringProperty()
    answerTwo = db.StringProperty()
    answerThree = db.StringProperty()
    which_user = db.UserProperty()
