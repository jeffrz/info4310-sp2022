# app.py
from flask import *
from whitenoise import WhiteNoise
import random, io, csv

from flask_sqlalchemy import SQLAlchemy  # helper functions for db access via postgres
from flask_heroku import Heroku  # helper functions for configuring flask for heroku
from flask_compress import Compress  # helper functions for compressing server responses
from flask_cors import CORS  # helper functions for cross-origin requests

app = Flask( __name__ )
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['COMPRESS_MIMETYPES'] = ['text/html','text/css','text/plain']
app.wsgi_app = WhiteNoise(app.wsgi_app, root='static/', prefix='static/', index_file="index.htm", autorefresh=True)
heroku = Heroku(app)
compress = Compress(app)
cors = CORS(app)
db = SQLAlchemy(app)

# put your database class at the top of the file
# one entry per survey response
class Entry(db.Model):
    __tablename__= "colorData"  # table within DB where data reside
    
    # specify columns for each row of data in the table
    id = db.Column(db.Integer, primary_key=True)
    colorValue = db.Column(db.String(8), nullable=False)
    colorName = db.Column(db.String(40), nullable=False)
    genderIdentity = db.Column(db.String(2), nullable=False)
    colorBlind = db.Column(db.String(10), nullable=False)
    surveyType = db.Column(db.String(20), nullable=False)
    
    # init makes it easier to make a row later in the code
    def __init__(self, colVal, colName, genIdent, colBlind, survType):
        self.colorValue = colVal
        self.colorName = colName
        self.genderIdentity = genIdent
        self.colorBlind = colBlind
        self.surveyType = survType
    
    # this function spits out an array of the data we put in the CSV file
    def getRow(self):
        return [self.colorValue, self.colorName, self.genderIdentity, self.colorBlind, self.surveyType]
    


@app.route('/', methods=['GET'])
def hello():
    return make_response("Greetings.")
    
    
def randomChroma():
    # Random function to generate fully saturated colors on surface of color cube
    r = random.randint(0,255)
    g = random.randint(0,255)
    b = random.randint(0,255)
    
    # The intuition here is that fully saturated colors MUST have either a 0 or 255 value on
    #  at least one of the color channels (so that it's on one of the sides of the cube)
    c = random.choice(['r','g','b'])
    if random.randint(0,1) == 0:
        if c == 'r':
            r = 0
        elif c == 'g':
            g = 0
        elif c == 'b':
            b = 0    
    else:
        if c == 'r':
            r = 255
        elif c == 'g':
            g = 255
        elif c == 'b':
            b = 255
    
    return '#%02x%02x%02x' % (r, g, b)
     

# serve one of two survey templates to the user randomly
#  if they have POSTed data using a form, save that data in the DB and then serve a template
@app.route('/survey', methods=['POST', 'GET'])
def survey():
    
    # handle survey form responses
    if request.method == "POST":
        print(request.form)
        
        # unpack using the "name" attrs on form inputs
        surveyType = request.form['surveyType']
        colName = request.form['colorName']
        colValue = request.form['colorValue']
        genIdent = request.form['genderIdent']
        colBlind = request.form['colorBlind']
        
        # Make an entry and commit it
        e = Entry(colValue, colName, genIdent, colBlind, surveyType)
        try:  # always put adding and saving changes in a try block
            db.session.add(e)
            db.session.commit()
        except Exception as e:
            print("\n FAILED entry: {}\n".format(json.dumps(data)))
            print(e)
            sys.stdout.flush()
            
    # if they aren't POST-ing, then we don't have any pulldown answers to save. make them the default blank
    else:
        genIdent = ""
        colBlind = ""
    
    
    # send a new survey to the user
    surveyTemplate = 'color_name_survey.htm'
    
    # pick a random color to put in the block of color
    colName = ""
    colVal = randomChroma()    # old: "#" + "%06x" % random.randint(0, 0xFFFFFF)
    
    # render template processes the htm file in the templates folder and fills in values
    #  this template uses {{ colorVal }} and some conditional statements for gender and colorblind
    return render_template('color_name_survey.htm', colorName=colName,
                                                    colorVal=colVal, 
                                                    genderIdent=genIdent, 
                                                    colorBlind=colBlind)
    

# send a CSV of the database entries to the user
#  usually not a good idea to publish raw DB contents, but here we have no identifiable information hopefully
@app.route('/dump_data')    
def dump():
    
    output = io.StringIO()  # this is an empty receptacle for string contents
    writer = csv.writer(output)  # we feed in the output of the writer to the receptacle
    writer.writerow( ['colorValue','colorName','genderIdentity','colorBlind','surveyType'] )
    
    # loop through all Entry rows in their table
    entries = Entry.query.all()
    for e in entries:
        writer.writerow( e.getRow() )
    
    # compose a response
    response = make_response( output.getvalue() )
    response.headers['Content-Type'] = 'text/plain'  # specify a MIME type so the browser knows how to present it
    return response
        

if __name__ == "__main__":
    app.run(threaded=True, port=5000)
