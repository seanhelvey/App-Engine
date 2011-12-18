#Sean Helvey
#N12031782

#------------------------------------------------------------
#comments are meant for you, the developer, not for users..
#Users please see UserGuide.otd in the project folder!
#Developers can refer DeveloperGuide.otd for more information.

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.ext.db import djangoforms 

import surveyDB
import cgitb
cgitb.enable()

#------------------------------------------------------------
#SurveyForm class
#It would be redundant to define fields in both model and form.
#Here we create SurveyForm with a Django helper class.
#Excluded fields are not displayed to the user in the form.
class SurveyForm(djangoforms.ModelForm):                                     
    class Meta:                                                                
        model = surveyDB.FrontPage
        exclude = ['choice','which_user','submit','results', 'q1a1X', 'q1a2X', 'q1a3X' \
                  , 'q2a1X', 'q2a2X', 'q2a3X', 'q3a1X', 'q3a2X', 'q3a3X']

#------------------------------------------------------------
#SurveyInputPage class
#Defining a request handler class to handle requests
class SurveyInputPage(webapp.RequestHandler):

    #Called to handle an HTTP GET request. Overridden by handler subclasses.
    def get(self):

        html = template.render('templates/header.html', {})
        html = html + '<div id="wrapper">'
        html = html + template.render('templates/form_start.html', {'action':'/'})

        #This gives us all surveys
        surveys = db.GqlQuery("SELECT * FROM FrontPage WHERE name != ''")
        html = html +  "<h3>Do you want to take one of these surveys?<br></h3>"

        #Radio if user wants to take survey
        for survey in surveys:
            x = survey.name
            x = x.replace(" ","_")
            html = html + "<INPUT TYPE=RADIO NAME='choice' VALUE=" + x + "> %s" %survey.name + "<br>"
            
        #String fields if users wants to make survey
        html = html +  "<h3>Or would you like to make your own survey?<br></h3>"
        html = html + str(SurveyForm(auto_id=False))
        html = html + template.render('templates/form_end.html', {'sub_title': 'Submit'})
        html = html + '</div>'
        html = html + template.render('templates/footer.html', {'links': ''})
        self.response.out.write(html)

    #Called to handle an HTTP POST request. Overridden by handler subclasses.
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
                currentUser = users.get_current_user()
                userAnswered = db.GqlQuery("SELECT * FROM FrontPage WHERE which_user != ''")

                z = survey.name
                z = z.replace(" ","_")

                #take the survey that is chosen by the user
                if y == z:
                    html = template.render('templates/header.html', {})        
                    html = html + template.render('templates/form_start.html', {})
                    
                    if(survey.q1 != ''):
                        html = html + survey.q1 + "<br>"
                    
                    if(survey.q1a1 != ''):
                        survey.q1a1 = survey.q1a1.replace(" ","_")

                        #disable
                        disabled = 0
                        for answer in userAnswered:
                            if(str(answer.which_user) == str(currentUser) and answer.q1a1 == survey.q1a1 and answer.name == '' and answer.choice == '' ):
                                html = html + "<INPUT TYPE=checkbox NAME='q1a1' VALUE=" + survey.q1a1 + " DISABLED> %s" %survey.q1a1 + "<br>"
                                disabled = 1
                        #enable
                        if disabled == 0:
                            html = html + "<INPUT TYPE=checkbox NAME='q1a1' VALUE=" + survey.q1a1 + "> %s" %survey.q1a1 + "<br>"   

                    if(survey.q1a2 != ''):
                        survey.q1a2 = survey.q1a2.replace(" ","_")

                        #disable
                        disabled = 0
                        for answer in userAnswered:
                            if(str(answer.which_user) == str(currentUser) and answer.q1a2 == survey.q1a2 and answer.name == '' and answer.choice == '' ):
                                html = html + "<INPUT TYPE=checkbox NAME='q1a2' VALUE=" + survey.q1a2 + " DISABLED> %s" %survey.q1a2 + "<br>"
                                disabled = 1
                        #enable
                        if disabled == 0:
                            html = html + "<INPUT TYPE=checkbox NAME='q1a2' VALUE=" + survey.q1a2 + "> %s" %survey.q1a2 + "<br>"   
                
                    if(survey.q1a3 != ''):
                        survey.q1a3 = survey.q1a3.replace(" ","_")

                        #disable
                        disabled = 0
                        for answer in userAnswered:
                            if(str(answer.which_user) == str(currentUser) and answer.q1a3 == survey.q1a3 and answer.name == '' and answer.choice == '' ):
                                html = html + "<INPUT TYPE=checkbox NAME='q1a3' VALUE=" + survey.q1a3 + " DISABLED> %s" %survey.q1a3 + "<br>"
                                disabled = 1
                        #enable
                        if disabled == 0:
                            html = html + "<INPUT TYPE=checkbox NAME='q1a3' VALUE=" + survey.q1a3 + "> %s" %survey.q1a3 + "<br>"   

                    if(survey.q2 != ''):
                        html = html + survey.q2 + "<br>"

                    if(survey.q2a1 != ''):
                        survey.q2a1 = survey.q2a1.replace(" ","_")

                        #disable
                        disabled = 0
                        for answer in userAnswered:
                            if(str(answer.which_user) == str(currentUser) and answer.q2a1 == survey.q2a1 and answer.name == '' and answer.choice == '' ):
                                html = html + "<INPUT TYPE=checkbox NAME='q2a1' VALUE=" + survey.q2a1 + " DISABLED> %s" %survey.q2a1 + "<br>"
                                disabled = 1
                        #enable
                        if disabled == 0:
                            html = html + "<INPUT TYPE=checkbox NAME='q2a1' VALUE=" + survey.q2a1 + "> %s" %survey.q2a1 + "<br>"   
                    
                    if(survey.q2a2 != ''):                        
                        survey.q2a2 = survey.q2a2.replace(" ","_")

                        #disable
                        disabled = 0
                        for answer in userAnswered:
                            if(str(answer.which_user) == str(currentUser) and answer.q2a2 == survey.q2a2 and answer.name == '' and answer.choice == '' ):
                                html = html + "<INPUT TYPE=checkbox NAME='q2a2' VALUE=" + survey.q2a2 + " DISABLED> %s" %survey.q2a2 + "<br>"
                                disabled = 1
                        #enable
                        if disabled == 0:
                            html = html + "<INPUT TYPE=checkbox NAME='q2a2' VALUE=" + survey.q2a2 + "> %s" %survey.q2a2 + "<br>"   

                    if(survey.q2a3 != ''):
                        survey.q2a3 = survey.q2a3.replace(" ","_")

                        #disable
                        disabled = 0
                        for answer in userAnswered:
                            if(str(answer.which_user) == str(currentUser) and answer.q2a3 == survey.q2a3 and answer.name == '' and answer.choice == '' ):
                                html = html + "<INPUT TYPE=checkbox NAME='q2a3' VALUE=" + survey.q2a3 + " DISABLED> %s" %survey.q2a3 + "<br>"
                                disabled = 1
                        #enable
                        if disabled == 0:
                            html = html + "<INPUT TYPE=checkbox NAME='q2a3' VALUE=" + survey.q2a3 + "> %s" %survey.q2a3 + "<br>"   

                    if(survey.q3 != ''):
                        html = html + survey.q3 + "<br>"

                    if(survey.q3a1 != ''):
                        survey.q3a1 = survey.q3a1.replace(" ","_")

                        #disable
                        disabled = 0
                        for answer in userAnswered:
                            if(str(answer.which_user) == str(currentUser) and answer.q3a1 == survey.q3a1 and answer.name == '' and answer.choice == '' ):
                                html = html + "<INPUT TYPE=checkbox NAME='q3a1' VALUE=" + survey.q3a1 + " DISABLED> %s" %survey.q3a1 + "<br>"
                                disabled = 1
                        #enable
                        if disabled == 0:
                            html = html + "<INPUT TYPE=checkbox NAME='q3a1' VALUE=" + survey.q3a1 + "> %s" %survey.q3a1 + "<br>"   

                    if(survey.q3a2 != ''):
                        survey.q3a2 = survey.q3a2.replace(" ","_")

                        #disable
                        disabled = 0
                        for answer in userAnswered:
                            if(str(answer.which_user) == str(currentUser) and answer.q3a2 == survey.q3a2 and answer.name == '' and answer.choice == '' ):
                                html = html + "<INPUT TYPE=checkbox NAME='q3a2' VALUE=" + survey.q3a2 + " DISABLED> %s" %survey.q3a2 + "<br>"
                                disabled = 1
                        #enable
                        if disabled == 0:
                            html = html + "<INPUT TYPE=checkbox NAME='q3a2' VALUE=" + survey.q3a2 + "> %s" %survey.q3a2 + "<br>"   

                    if(survey.q3a3 != ''):
                        survey.q3a3 = survey.q3a3.replace(" ","_")

                        #disable
                        disabled = 0
                        for answer in userAnswered:
                            if(str(answer.which_user) == str(currentUser) and answer.q3a3 == survey.q3a3 and answer.name == '' and answer.choice == '' ):
                                html = html + "<INPUT TYPE=checkbox NAME='q3a3' VALUE=" + survey.q3a3 + " DISABLED> %s" %survey.q3a3 + "<br>"
                                disabled = 1
                        #enable
                        if disabled == 0:
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

#----------------------------------------
#Counter is used in ResultsPage below
class Counter(object):
    def __init__(self, name=None):
        self.name = name
        self.q1a1 = 0
        self.q1a2 = 0
        self.q1a3 = 0
        self.q2a1 = 0
        self.q2a2 = 0
        self.q2a3 = 0
        self.q3a1 = 0
        self.q3a2 = 0
        self.q3a3 = 0

#----------------------------------------
#ResultsPage calculates and displays results 
class ResultsPage(webapp.RequestHandler):
    def get(self):
        surveys = db.GqlQuery("SELECT * FROM FrontPage WHERE name != ''")        
        responses = db.GqlQuery("SELECT * FROM FrontPage WHERE name = '' AND choice = ''")
        #html = template.render('templates/header.html', {})

        counterList = []

        for survey in surveys:

            counterList.append(Counter(survey.name))

            for response in responses:
                survey.q1a1 = survey.q1a1.replace(" ","_")
                response.q1a1 = response.q1a1.replace(" ","_")
                if survey.q1a1 == response.q1a1 and survey.q1a1 != '' and response.q1a1 != '' :
                    for counter in counterList:
                        if counter.name == survey.name:
                            counter.q1a1 = counter.q1a1 + 1

                survey.q1a2 = survey.q1a2.replace(" ","_")
                response.q1a2 = response.q1a2.replace(" ","_")
                if survey.q1a2 == response.q1a2 and survey.q1a2 != '' and response.q1a2 != '' :
                    for counter in counterList:
                        if counter.name == survey.name:
                            counter.q1a2 = counter.q1a2 + 1

                survey.q1a3 = survey.q1a3.replace(" ","_")
                response.q1a3 = response.q1a3.replace(" ","_")
                if survey.q1a3 == response.q1a3 and survey.q1a3 != '' and response.q1a3 != '' :
                    for counter in counterList:
                        if counter.name == survey.name:
                            counter.q1a3 = counter.q1a3 + 1

                survey.q2a1 = survey.q2a1.replace(" ","_")
                response.q2a1 = response.q2a1.replace(" ","_")
                if survey.q2a1 == response.q2a1 and survey.q2a1 != '' and response.q2a1 != '' :
                    for counter in counterList:
                        if counter.name == survey.name:
                            counter.q2a1 = counter.q2a1 + 1

                survey.q2a2 = survey.q2a2.replace(" ","_")
                response.q2a2 = response.q2a2.replace(" ","_")
                if survey.q2a2 == response.q2a2 and survey.q2a2 != '' and response.q2a2 != '' :
                    for counter in counterList:
                        if counter.name == survey.name:
                            counter.q2a2 = counter.q2a2 + 1

                survey.q2a3 = survey.q2a3.replace(" ","_")
                response.q2a3 = response.q2a3.replace(" ","_")
                if survey.q2a3 == response.q2a3 and survey.q2a3 != '' and response.q2a3 != '' :
                    for counter in counterList:
                        if counter.name == survey.name:
                            counter.q2a3 = counter.q2a3 + 1

                survey.q3a1 = survey.q3a1.replace(" ","_")
                response.q3a1 = response.q3a1.replace(" ","_")
                if survey.q3a1 == response.q3a1 and survey.q3a1 != '' and response.q3a1 != '' :
                    for counter in counterList:
                        if counter.name == survey.name:
                            counter.q3a1 = counter.q3a1 + 1

                survey.q3a2 = survey.q3a2.replace(" ","_")
                response.q3a2 = response.q3a2.replace(" ","_")
                if survey.q3a2 == response.q3a2 and survey.q3a2 != '' and response.q3a2 != '' :
                    for counter in counterList:
                        if counter.name == survey.name:
                            counter.q3a2 = counter.q3a2 + 1

                survey.q3a3 = survey.q3a3.replace(" ","_")
                response.q3a3 = response.q3a3.replace(" ","_")
                if survey.q3a3 == response.q3a3 and survey.q3a3 != '' and response.q3a3 != '' :
                    for counter in counterList:
                        if counter.name == survey.name:
                            counter.q3a3 = counter.q3a3 + 1

        #------------------------------------------------------------
        #Begin javascript pie chart
      
        html = """
      <html><head><title></title>
      <link type="text/css" rel="stylesheet" href="/static/surveyMod.css" />

    <!--Load the AJAX API-->
    <script type="text/javascript" src="https://www.google.com/jsapi"></script>
    <script type="text/javascript">

      // Load the Visualization API and the piechart package.
      google.load('visualization', '1.0', {'packages':['corechart']});

      // Set a callback to run when the Google Visualization API is loaded.
      google.setOnLoadCallback(drawChart);

      // Callback that creates and populates a data table,
      // instantiates the pie chart, passes in the data and
      // draws it.
      function drawChart() {

      num = 1;"""

        #This is actually happening within the JS funtion drawChart()
        for survey in surveys:

            html = html + """// Create the data table.

      eval("var dataA" + num + "= new google.visualization.DataTable();");
      eval("var dataB" + num + "= new google.visualization.DataTable();");
      eval("var dataC" + num + "= new google.visualization.DataTable();");

      eval("dataA" + num + ".addColumn('string', 'Answer');");
      eval("dataB" + num + ".addColumn('string', 'Answer');");
      eval("dataC" + num + ".addColumn('string', 'Answer');");

      eval("dataA" + num + ".addColumn('number', 'Number');");
      eval("dataB" + num + ".addColumn('number', 'Number');");
      eval("dataC" + num + ".addColumn('number', 'Number');");

      eval("variableA = dataA" + num + ";");
      eval("variableB = dataB" + num + ";");
      eval("variableC = dataC" + num + ";");

      html = html + """
 
            #The html below can be uncommented or controlled using statements.
            #Text would be displayed correctly if the comments were removed.
            #This may be desireable as currently the JS only displays in Firefox
            if (survey.q1a1 != '') or (survey.q1a2 != '') or (survey.q1a3 != '') \
            or (survey.q2a1 != '') or (survey.q2a2 != '') or (survey.q2a3 != '') \
            or (survey.q3a1 != '') or (survey.q3a2 != '') or (survey.q3a3 != '') :
                #html = html + survey.name + "<br>"
                x=2

            if (survey.q1a1 != '') or (survey.q1a2 != '') or (survey.q1a3 != ''):
                #html = html + survey.q1 + "<br>"
                x=2

            if (survey.q1a1 != ''):
                for counter in counterList:
                    if counter.name == survey.name:
                        #html = html + survey.q1a1 + " " + str(counter.q1a1) + "<br>"
                        #Note this is still part of the Javascript here in quotes below
                        html = html + "variableA.addRows([['"+ survey.q1a1 + "'," + str(counter.q1a1) + "]]);"
                        x=2
                        
            if (survey.q1a2 != ''):
                for counter in counterList:
                    if counter.name == survey.name:
                        #html = html + survey.q1a2 + " " + str(counter.q1a2) + "<br>"
                        html = html + "variableA.addRows([['"+ survey.q1a2 + "'," + str(counter.q1a2) + "]]);"
                        x=2
                        
            if (survey.q1a3 != ''):
                for counter in counterList:
                    if counter.name == survey.name:
                        #html = html + survey.q1a3 + " " + str(counter.q1a3) + "<br>"
                        html = html + "variableA.addRows([['"+ survey.q1a3 + "'," + str(counter.q1a3) + "]]);"
                        x=2

            if (survey.q2a1 != '') or (survey.q2a2 != '') or (survey.q2a3 != ''):
                #html = html + survey.q2 + "<br>"
                x=2

            if (survey.q2a1 != ''):
                for counter in counterList:
                    if counter.name == survey.name:
                        #html = html + survey.q2a1 + " " + str(counter.q2a1) + "<br>"
                        html = html + "variableB.addRows([['"+ survey.q2a1 + "'," + str(counter.q2a1) + "]]);"
                        x=2

            if (survey.q2a2 != ''):
                for counter in counterList:
                    if counter.name == survey.name:
                        #html = html + survey.q2a2 + " " + str(counter.q2a2) + "<br>"
                        html = html + "variableB.addRows([['"+ survey.q2a2 + "'," + str(counter.q2a2) + "]]);"
                        x=2

            if (survey.q2a3 != ''):
                for counter in counterList:
                    if counter.name == survey.name:
                        #html = html + survey.q2a3 + " " + str(counter.q2a3) + "<br>"
                        html = html + "variableB.addRows([['"+ survey.q2a3 + "'," + str(counter.q2a3) + "]]);"
                        x=2

            if (survey.q3a1 != '') or (survey.q3a2 != '') or (survey.q3a3 != ''):
                #html = html + survey.q3 + "<br>"
                x=2

            if (survey.q3a1 != ''):
                for counter in counterList:
                    if counter.name == survey.name:
                        #html = html + survey.q3a1 + " " + str(counter.q3a1) + "<br>"
                        html = html + "variableC.addRows([['"+ survey.q3a1 + "'," + str(counter.q3a1) + "]]);"
                        x=2

            if (survey.q3a2 != ''):
                for counter in counterList:
                    if counter.name == survey.name:
                        #html = html + survey.q3a2 + " " + str(counter.q3a2) + "<br>"
                        html = html + "variableC.addRows([['"+ survey.q3a2 + "'," + str(counter.q3a2) + "]]);"
                        x=2

            if (survey.q3a3 != ''):
                for counter in counterList:
                    if counter.name == survey.name:
                        #html = html + survey.q3a3 + " " + str(counter.q3a3) + "<br>"
                        html = html + "variableC.addRows([['"+ survey.q3a3 + "'," + str(counter.q3a3) + "]]);"
                        x=2

            html = html + """
            
      // Set chart options
      eval("var optionsA" + num + "= {'title':'""" + survey.q1 + """','width':400,'height':300};");
      eval("var optionsB" + num + "= {'title':'""" + survey.q2 + """','width':400,'height':300};");
      eval("var optionsC" + num + "= {'title':'""" + survey.q3 + """','width':400,'height':300};");

      // Instantiate and draw our chart, passing in some options.
      eval("var chartA" + num + "= new google.visualization.PieChart(document.getElementById('chart_divA" + num + "'));");
      eval("chartA" + num + ".draw(dataA" + num + ", optionsA" + num + ");");
      eval("var chartB" + num + "= new google.visualization.PieChart(document.getElementById('chart_divB" + num + "'));");
      eval("chartB" + num + ".draw(dataB" + num + ", optionsB" + num + ");");
      eval("var chartC" + num + "= new google.visualization.PieChart(document.getElementById('chart_divC" + num + "'));");
      eval("chartC" + num + ".draw(dataC" + num + ", optionsC" + num + ");");
      num = num + 1;"""

        #curly brace here below is end of prior javascript function
        html = html + '}</script></head><body>'

        number = 1
        for survey in surveys:
            html = html + survey.name + "<br>"
            html = html + '<div id="chart_divA' + str(number) + '"></div>'
            html = html + '<div id="chart_divB' + str(number) + '"></div>'
            html = html + '<div id="chart_divC' + str(number) + '"></div>'
            number = number + 1

        html = html + '</body></html>'

        self.response.out.write(html)

app = webapp.WSGIApplication([('/', SurveyInputPage),('/results',ResultsPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()
