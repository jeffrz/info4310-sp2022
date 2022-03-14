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

# DB CODE HERE!




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
    pass
    

# send a CSV of the database entries to the user
#  usually not a good idea to publish raw DB contents, but here we have no identifiable information hopefully
@app.route('/dump_data')    
def dump():
    pass
        

if __name__ == "__main__":
    app.run(threaded=True, port=5000)
