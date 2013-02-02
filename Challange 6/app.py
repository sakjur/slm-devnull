from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy
import urllib2, urllib
import json

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

    urlstars = urllib2.urlopen(uri + "/api2/?session=" + sid + "&command=longrange")
    urlship = urllib2.urlopen(uri + "/api2/?session=" + sid + "&command=ship&arg=show")
    ship = urlship.read()

    if flyTo:
        planchoice = flyTo.replace(" ", "%20")
        urlflyTo = urllib2.urlopen(uri + "/api2/?session=" + sid + "&command=ship&arg=setsystemdest&arg2=" + planchoice)

    return render_template('planetsystem.html', short=short, ship=ship)

def createDbStars():
    urlstars = urllib2.urlopen(uri + "/api2/?session=" + sid + "&command=longrange")
    urlstars = json.load(urlstars)

    for each in urlstars.values():
        for item in each:
            addition = Star(item)
            db.session.add(addition)

    db.session.commit()

def createDbPlanets():
    urlshort = urllib2.urlopen(uri + "/api2/?session=" + sid + "&command=shortrange")
    urlshort = json.load(urlshort)

    for each in urlshort.values():
        for item in each:
            addition = Planet(item)
            db.session.add(addition)

    db.session.commit()

class Star(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    x = db.Column(db.Integer)
    y = db.Column(db.Integer)
    planets = db.Column(db.Integer)
    starClass = db.Column(db.String(50))
    name = db.Column(db.String(80), unique=True)

    def __init__(self, dictionary):
        self.x = int(dictionary["x"])
        self.y = int(dictionary["y"])
        self.planets = str(dictionary["planets"])
        self.starClass = str(dictionary["class"])
        self.name = str(dictionary["name"])

class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    a = db.Column(db.Float)
    albedo = db.Column(db.Float)
    atmosphere = db.Column(db.Float)
    axial_tilt = db.Column(db.Float)
    boil_point = db.Column(db.Float)
    core_radius = db.Column(db.Float)
    density = db.Column(db.Float)
    dust_mass = db.Column(db.Float)
    e = db.Column(db.Float)
    estimated_temp = db.Column(db.Float)
    estimated_terr_temp = db.Column(db.Float)
    exospheric_temp = db.Column(db.Float)
    gas_giant = db.Column(db.Integer)
    gass_mass = db.Column(db.Float)
    greenhouse_effect = db.Column(db.Integer)
    greenhs_rise = db.Column(db.Float)
    high_temp = db.Column(db.Float)
    hydrosphere = db.Column(db.Float)
    ice_cover = db.Column(db.Float)
    low_temp = db.Column(db.Float)
    mass = db.Column(db.Float)
    max_temp = db.Column(db.Float)
    min_temp = db.Column(db.Float)
    minor_moons = db.Column(db.Integer)
    molec_weight = db.Column(db.Float)
    orb_period = db.Column(db.Float)
    resonant_period = db.Column(db.Integer)
    rms_velocity = db.Column(db.Float)
    surf_accel = db.Column(db.Float)
    surf_pressure = db.Column(db.Float)
    surf_temp = db.Column(db.Float)
    volatile_gas_inventory = db.Column(db.Float)
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
