
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

        html = template.render('templates/header.html', {})
        html = html + '<div id="wrapper">'
        html = html + template.render('templates/form_start.html', {})
        surveys = db.GqlQuery("SELECT * FROM FrontPage WHERE name != ''")
        html = html +  "<h3>Do you want to take one of these surveys?<br></h3>"

        for survey in surveys:
            x = survey.name
            x = x.replace(" ","_")
            html = html + "<INPUT TYPE=RADIO NAME='choice' VALUE=" + x + "> %s" %survey.name + "<br>"
            
        html = html +  "<h3>Or would you like to make your own survey?<br></h3>"
        html = html + str(SurveyForm(auto_id=False))
        html = html + template.render('templates/form_end.html', {'sub_title': 'Submit'})
        html = html + '</div>'
        html = html + template.render('templates/footer.html', {'links': ''})
        self.response.out.write(html)

    def post(self): 
        
        front_page = surveyDB.FrontPage()
        front_page.name = self.request.get('name')

        front_page.q1 = self.request.get('q1')
        front_page.q1a1 = self.request.get('q1a1')
        front_page.q1a2 = self.request.get('q1a2')
        front_page.q1a3 = self.request.get('q1a3')

        front_page.q2 = self.request.get('q2')
        front_page.q2a1 = self.request.get('q2a1')
        front_page.q2a2 = self.request.get('q2a2')
        front_page.q2a3 = self.request.get('q2a3')

        front_page.q3 = self.request.get('q3')
        front_page.q3a1 = self.request.get('q3a1')
        front_page.q3a2 = self.request.get('q3a2')
        front_page.q3a3 = self.request.get('q3a3')

        y = self.request.get('choice')
        front_page.choice = y
        front_page.which_user = users.get_current_user()
        front_page.put()
        
        surveys = db.GqlQuery("SELECT * FROM FrontPage WHERE name != ''")        
        html = template.render('templates/header.html', {})
        
        for survey in surveys:
            z = survey.name
            z = z.replace(" ","_")
            if y == z:
                print survey.name
                print survey.q1
                print survey.q1a1
                print survey.q1a2
                print survey.q1a3

        html = html + template.render('templates/footer.html',
                                      {'links': 'Enter <a href="/">another</a>.'})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', SurveyInputPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()
