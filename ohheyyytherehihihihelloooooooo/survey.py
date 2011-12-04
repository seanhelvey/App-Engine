
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
        model = surveyDB.Survey
        exclude = ['choice','which_user']

class SurveyInputPage(webapp.RequestHandler):
    def get(self):
        html = template.render('templates/header.html', {'title': 'SURVEY'})
        html = html + template.render('templates/form_start.html', {})
        surveys = db.GqlQuery("SELECT * FROM Survey")
        html = html +  "<h2>Do you want to take one of these surveys?<br></h2>"

        for survey in surveys:
            html = html + "<INPUT TYPE=RADIO NAME='SurveyInputPage' VALUE="
            html = html + str(survey.question) + "> %s <br>" %survey.question + "<br>"
            
        html = html +  "<h2>Or would you like to make your own survey??<br></h2>"
        html = html + str(SurveyForm(auto_id=False))
        html = html + template.render('templates/form_end.html', {'sub_title': 'Submit'})
        html = html + template.render('templates/footer.html', {'links': ''})
        self.response.out.write(html)

    def post(self): 
        new_survey = surveyDB.Survey()
        
        if(self.request.get('question') == ''):
            new_survey.choice = self.request.get('choice')

        else:
            new_survey.question = self.request.get('question')
            new_survey.answerOne = self.request.get('answerOne')
            new_survey.answerTwo = self.request.get('answerTwo')
            new_survey.answerThree = self.request.get('answerThree')
        
        new_survey.which_user = users.get_current_user()

        new_survey.put()
        
        html = template.render('templates/header.html', {'title': 'Thank you!'})
        html = html + template.render('templates/footer.html',
                                      {'links': 'Enter <a href="/">another</a>.'})
        self.response.out.write(html)        
        
app = webapp.WSGIApplication([('/.*', SurveyInputPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()
