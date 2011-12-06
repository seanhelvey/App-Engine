
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
        exclude = ['choice','which_user','submit','results']

class SurveyInputPage(webapp.RequestHandler):
    def get(self):

        html = template.render('templates/header.html', {})
        html = html + '<div id="wrapper">'
        html = html + template.render('templates/form_start.html', {'action':'/'})
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

        #if the user chose a survey to take
        if y != '':   

            #get all of the surveys in the datastore
            surveys = db.GqlQuery("SELECT * FROM FrontPage WHERE name != ''")
            for survey in surveys:
                z = survey.name
                z = z.replace(" ","_")

                #take the survey that is chosen by the user
                if y == z:
                    html = template.render('templates/header.html', {})        
                    #html = html + template.render('templates/form_start.html', {'action':'/results'})
                    html = html + template.render('templates/form_start.html', {})

                    if(survey.q1 != ''):
                        html = html + survey.q1 + "<br>"
                    
                    if(survey.q1a1 != ''):
                        html = html + "<INPUT TYPE=checkbox NAME='q1a1' VALUE=" + survey.q1a1 + "> %s" %survey.q1a1 + "<br>"

                    if(survey.q1a2 != ''):
                        html = html + "<INPUT TYPE=checkbox NAME='q1a2' VALUE=" + survey.q1a2 + "> %s" %survey.q1a2 + "<br>"
                
                    if(survey.q1a3 != ''):
                        html = html + "<INPUT TYPE=checkbox NAME='q1a3' VALUE=" + survey.q1a3 + "> %s" %survey.q1a3 + "<br>"

                    if(survey.q2 != ''):
                        html = html + survey.q2 + "<br>"

                    if(survey.q2a1 != ''):
                        html = html + "<INPUT TYPE=checkbox NAME='q2a1' VALUE=" + survey.q2a1 + "> %s" %survey.q2a1 + "<br>"
                    
                    if(survey.q2a2 != ''):                        
                        html = html + "<INPUT TYPE=checkbox NAME='q2a2' VALUE=" + survey.q2a2 + "> %s" %survey.q2a2 + "<br>"

                    if(survey.q2a3 != ''):
                        html = html + "<INPUT TYPE=checkbox NAME='q2a3' VALUE=" + survey.q2a3 + "> %s" %survey.q2a3 + "<br>"

                    if(survey.q3 != ''):
                        html = html + survey.q3 + "<br>"

                    if(survey.q3a1 != ''):
                        html = html + "<INPUT TYPE=checkbox NAME='q3a1' VALUE=" + survey.q3a1 + "> %s" %survey.q3a1 + "<br>"

                    if(survey.q3a2 != ''):
                        html = html + "<INPUT TYPE=checkbox NAME='q3a2' VALUE=" + survey.q3a2 + "> %s" %survey.q3a2 + "<br>"

                    if(survey.q3a3 != ''):
                        html = html + "<INPUT TYPE=checkbox NAME='q3a3' VALUE=" + survey.q3a3 + "> %s" %survey.q3a3 + "<br>"

                    html = html + template.render('templates/form_pre_end.html', {'name': 'Submit','sub_title': 'Submit'})
                    html = html + template.render('templates/form_end.html', {'name': 'Submit', 'sub_title': 'Results'})

                    html = html + template.render('templates/footer.html',{'links': 'Enter <a href="/">another</a>'})
                    self.response.out.write(html)
                    
        #the user chose to enter a new survey
        else:
            html = template.render('templates/header.html', {})        
            html = html + template.render('templates/footer.html',{'links': 'Enter <a href="/results">results</a>.'})            
            self.response.out.write(html)

class ResultsPage(webapp.RequestHandler):
    def get(self):
        surveys = db.GqlQuery("SELECT * FROM FrontPage WHERE name != ''")        
        responses = db.GqlQuery("SELECT * FROM FrontPage WHERE name = '' AND choice = ''")
        html = "<html><head><title></title></head><body>"

        q1a1 = 0
        q1a2 = 0
        q1a3 = 0
        q2a1 = 0
        q2a2 = 0
        q2a3 = 0
        q3a1 = 0
        q3a2 = 0
        q3a3 = 0

        for survey in surveys:
            for response in responses:
                if survey.q1a1 == response.q1a1 and survey.q1a1 != '' and response.q1a1 != '' :
                    q1a1 = q1a1 + 1

                if survey.q1a2 == response.q1a2 and survey.q1a2 != '' and response.q1a2 != '' :
                    q1a2 = q1a2 + 1

                if survey.q1a3 == response.q1a3 and survey.q1a3 != '' and response.q1a3 != '' :
                    q1a3 = q1a3 + 1

                if survey.q2a1 == response.q2a1 and survey.q2a1 != '' and response.q2a1 != '' :
                    q2a1 = q2a1 + 1

                if survey.q2a2 == response.q2a2 and survey.q2a2 != '' and response.q2a2 != '' :
                    q2a2 = q2a2 + 1

                if survey.q2a3 == response.q2a3 and survey.q2a3 != '' and response.q2a3 != '' :
                    q2a3 = q2a3 + 1

                if survey.q3a1 == response.q3a1 and survey.q3a1 != '' and response.q3a1 != '' :
                    q3a1 = q3a1 + 1

                if survey.q3a2 == response.q3a2 and survey.q3a2 != '' and response.q3a2 != '' :
                    q3a2 = q3a2 + 1

                if survey.q3a3 == response.q3a3 and survey.q3a3 != '' and response.q3a3 != '' :
                    q3a3 = q3a3 + 1

        for survey in surveys:
            if (survey.q1a1 != ''):
                html = html + survey.q1a1 + " " + str(q1a1) + "<br>"

            if (survey.q1a2 != ''):
                html = html + survey.q1a2 + " " + str(q1a2) + "<br>"

            if (survey.q1a3 != ''):
                html = html + survey.q1a3 + " " + str(q1a3) + "<br>"

            if (survey.q2a1 != ''):
                html = html + survey.q2a1 + " " + str(q2a1) + "<br>"

            if (survey.q2a2 != ''):
                html = html + survey.q2a2 + " " + str(q2a2) + "<br>"

            if (survey.q2a3 != ''):
                html = html + survey.q2a3 + " " + str(q2a3) + "<br>"

            if (survey.q3a1 != ''):
                html = html + survey.q3a1 + " " + str(q3a1) + "<br>"

            if (survey.q3a2 != ''):
                html = html + survey.q3a2 + " " + str(q3a2) + "<br>"

            if (survey.q3a3 != ''):
                html = html + survey.q3a3 + " " + str(q3a3) + "<br>"

        html = html + "</body></html>"
        self.response.out.write(html)

app = webapp.WSGIApplication([('/', SurveyInputPage),('/results',ResultsPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()
