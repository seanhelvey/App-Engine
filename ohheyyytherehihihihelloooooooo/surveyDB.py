from google.appengine.ext import db

class FrontPage(db.Model):
    name = db.StringProperty()
    question = db.StringProperty()
    answerOne = db.StringProperty()
    answerTwo = db.StringProperty()
    answerThree = db.StringProperty()
    choice = db.StringProperty()
    which_user = db.UserProperty()
