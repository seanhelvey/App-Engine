
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.ext.db import djangoforms 

import surveyDB
import cgitb
cgitb.enable()

class SurveyForm(djangoforms.ModelForm):                                     
    class Meta:                                                                
        model = surveyDB.FrontPage
        exclude = ['choice','which_user']

class SurveyInputPage(webapp.RequestHandler):
    def get(self):
        html = template.render('templates/header.html', {'title': 'SURVEY'})
        html = html + template.render('templates/form_start.html', {})
        surveys = db.GqlQuery("SELECT * FROM FrontPage WHERE name != ''")
        html = html +  "<h2>Do you want to take one of these surveys?<br></h2>"

        for survey in surveys:
            x = survey.name
            x = x.replace(" ","_")
            html = html + "<INPUT TYPE=RADIO NAME='choice' VALUE=" + x + "> %s" %survey.name + "<br>"
            
        html = html +  "<h2>Or would you like to make your own survey?<br></h2>"
        html = html + str(SurveyForm(auto_id=False))
        html = html + template.render('templates/form_end.html', {'sub_title': 'Submit'})
        html = html + template.render('templates/footer.html', {'links': ''})
        self.response.out.write(html)

    def post(self): 
        
        front_page = surveyDB.FrontPage()
        front_page.name = self.request.get('name')
        front_page.question = self.request.get('question')
        front_page.answerOne = self.request.get('answerOne')
        front_page.answerTwo = self.request.get('answerTwo')
        front_page.answerThree = self.request.get('answerThree')
        front_page.choice = self.request.get('choice')
        front_page.which_user = users.get_current_user()
        front_page.put()
        
        html = template.render('templates/header.html', {'title': 'Thank you!'})
        html = html + template.render('templates/footer.html',
                                      {'links': 'Enter <a href="/">another</a>.'})
        self.response.out.write(html)        
        
app = webapp.WSGIApplication([('/.*', SurveyInputPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()
