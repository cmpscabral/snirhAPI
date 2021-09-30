from datetime import timedelta

from flask import Flask
from flask_restplus import Api
from flask_session import Session
from werkzeug.middleware.proxy_fix import ProxyFix

import redis

import os

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
api = Api(
    app,
    version="1.0",
    title="SNIRH API",
    description="An API to fetch hidrological data from <a href='https://snirh.apambiente.pt/'>SNIRH</a>. Check the source code <a href='https://github.com/franciscobmacedo/snirhapi'>here</a>",
)

ns = api.namespace("api", description="SNIRH API operations")

app.secret_key = "BAD_SECRET_KEY"

from dotenv import load_dotenv

load_dotenv()
WITH_REDIS_SESSION = os.environ.get("WITH_REDIS_SESSION")
if WITH_REDIS_SESSION:
    from flask import session

    app.config["SESSION_TYPE"] = "redis"
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_USE_SIGNER"] = True
    app.config["SESSION_REDIS"] = redis.from_url("redis://localhost:6379")
    server_session = Session(app)

    @app.before_request
    def make_session_permanent():
        session.permanent = True
        app.permanent_session_lifetime = timedelta(minutes=30)


else:
    session = {}


app.config["RESTPLUS_MASK_SWAGGER"] = False
