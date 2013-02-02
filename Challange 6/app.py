from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy
import urllib2, urllib

app = Flask(__name__)
uri = "https://lostinspace.lanemarknad.se:8000"
sid = "f6319047-1cfb-4bfa-ae4b-318355d2b90e"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/devnull.db'
db = SQLAlchemy(app)

@app.route("/")
@app.route("/<starchoice>")
def hello(starchoice=None):
    urlstars = urllib2.urlopen(uri + "/api2/?session=" + sid + "&command=longrange")
    stars = urlstars.read()

    urlship = urllib2.urlopen(uri + "/api2/?session=" + sid + "&command=ship&arg=show")
    ship = urlship.read()

    if starchoice:
        starchoice = starchoice.replace(" ", "%20")
        urllib2.urlopen(uri + "/api2/?session=" + sid + "&command=ship&arg=setunidest&arg2=" + starchoice)

    return render_template('starsystem.html', stars=stars, ship=ship)

@app.route("/current")
@app.route("/current/flyto/<flyTo>")
def currentSystem(flyTo=None):
    urlshort = urllib2.urlopen(uri + "/api2/?session=" + sid + "&command=shortrange")
    short = urlshort.read()

    urlship = urllib2.urlopen(uri + "/api2/?session=" + sid + "&command=ship&arg=show")
    ship = urlship.read()

    if flyTo:
        planchoice = flyTo.replace(" ", "%20")
        urlflyTo = urllib2.urlopen(uri + "/api2/?session=" + sid + "&command=ship&arg=setsystemdest&arg2=" + planchoice)

    return render_template('planetsystem.html', short=short, ship=ship)

class Star(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    x = db.Column(db.Integer)
    y = db.Column(db.Integer)
    planets = db.Column(db.Integer)
    starClass = db.Column(db.String(50))
    name = db.Column(db.String(80), unique=True)

class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    starid = db.Column(db.Integer)
    x = db.Column(db.Integer)
    y = db.Column(db.Integer)
    day = db.Column(db.Float)
    esc_velocity = db.Column(db.Float)
    cloud_cover = db.Column(db.Float)
    radius = db.Column(db.Float)
    type = db.Column(db.String(50))
    planet_no = db.Column(db.String(50))
    surf_grav = db.Column(db.Float)
    orbit_zone = db.Column(db.Integer)


if __name__ == "__main__":
    app.debug = True
    app.run()
