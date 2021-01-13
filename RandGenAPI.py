from flask import Flask, make_response, url_for, render_template, redirect, session
from flask_restplus import Api, Resource
import numpy as np
from authlib.integrations.flask_client import OAuth

from auth_decorator import login_required

version="v0"

swagger_url = f'/api/{version}/docs'
api_url = f"/api/{version}/RandGen/"

app = Flask(__name__, template_folder='templates')

api = Api(
    app, 
    version='1.0', 
    title='RandGen API',
    description='A simple Random Number Generator API.',
    doc=f'/api/{version}/docs/'
)

ns = api.namespace('RandGen', description='RandGen operations')

app.secret_key = 'aosboasbf54713r44567bfa'

# oAuth Setup
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id='927315565207-q2o21kpfds9vunnoshlgcff16517r9gc.apps.googleusercontent.com',
    client_secret='j25E_6Y3fbg4htbY_q0V7ZI9',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',  # This is only needed if using openId to fetch user info
    client_kwargs={'scope': 'openid email profile'},
)




@app.route('/login')
def login():
    google = oauth.create_client('google')  # create the google oauth client
    redirect_uri = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route('/authorize')
def authorize():
    google = oauth.create_client('google')  # create the google oauth client
    token = google.authorize_access_token()  # Access token from google (needed to get user info)
    resp = google.get('userinfo')  # userinfo contains stuff u specificed in the scrope
    user_info = resp.json()
    user = oauth.google.userinfo()  # uses openid endpoint to fetch user info
    # Here you use the profile/user data that you got and query your database find/register the user
    # and set ur own data in the session not the profile from google
    session['profile'] = user_info
    session.permanent = True  # make the session permanant so it keeps existing after broweser gets closed
    return redirect(swagger_url)

@app.route('/logout')
def logout():
    for key in list(session.keys()):
        session.pop(key)
    return redirect('/')



@ns.route(api_url)
class RandGen(Resource):
    
    @login_required
    def get(self):
        """Get a random number between 0 and 1.
        """    
        output = {
            'number' : np.random.rand()
        }
        return output




api.add_resource(RandGen, api_url)

app.run(debug=True)