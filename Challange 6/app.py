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
    stars = db2dict(Star.query.all())

    urlship = urllib2.urlopen(uri + "/api2/?session=" + sid + "&command=ship&arg=show")
    ship = urlship.read()

    if starchoice:
        starchoice = starchoice.replace(" ", "%20")
        urllib2.urlopen(uri + "/api2/?session=" + sid + "&command=ship&arg=setunidest&arg2=" + starchoice)

    return render_template('starsystem.html', stars=stars, ship=ship)

@app.route("/current")
@app.route("/current/flyto/<flyTo>")
def currentSystem(flyTo=None):
    urlstars = urllib2.urlopen(uri + "/api2/?session=" + sid + "&command=longrange")
    urlship = urllib2.urlopen(uri + "/api2/?session=" + sid + "&command=ship&arg=show")
    ship = urlship.read()
    pyship = json.loads(ship)

    for each in pyship.items():
        if each[0] == "currentsystem":
            currentsystem = str(each[1])
    
    cursys = Star.query.filter_by(name=currentsystem).first()
    if not cursys:
        pass
    else:
        cursysid = cursys.id

        exists = False
        for each in Planet.query.filter_by(starid=cursysid):
            if each:
                exists = True
            else:
                exists = False

        if not exists:
            fillDbStarsystem()

    urlshort = urllib2.urlopen(uri + "/api2/?session=" + sid + "&command=shortrange")
    short = urlshort.read()

    if flyTo:
        planchoice = flyTo.replace(" ", "%20")
        urlflyTo = urllib2.urlopen(uri + "/api2/?session=" + sid + "&command=ship&arg=setsystemdest&arg2=" + planchoice)

    return render_template('planetsystem.html', short=short, ship=ship)

@app.route('/scanplanet/')
def scanPlanet():
    urlship = urllib2.urlopen(uri + "/api2/?session=" + sid + "&command=ship&arg=show")
    ship = urlship.read()
    pyship = json.loads(ship)
    rv = ""

    for each in pyship.items():
        if each[0] == "currentplanet":
            currentplanet = str(each[1])
            rv += currentplanet
    
    if not planetInfo(currentplanet):
        fillPlanetData()
        rv += "Testar"
    return rv

@app.route('/planetinfo/<planet>')
def planetInfo(planet=None):
    if not planet:
        return ""
    planet = Planet.query.filter_by(planet_no=planet).first()
    if not planet:
        return ""

    planet = PlanDetails.query.filter_by(planetid=planet.id).first()
    rv = ""
    if planet:
        rv += "planetid: " + str(planet.planetid) + "<br />"
        rv += "a: " + str(planet.a) + "<br />"
        rv += "albedo: " + str(planet.albedo) + "<br />"
        rv += "atmosphere: " + str(planet.atmosphere) + "<br />"
        rv += "axial_tilt: " + str(planet.axial_tilt) + "<br />"
        rv += "boil_point: " + str(planet.boil_point) + "<br />"
        rv += "core_radius: " + str(planet.core_radius) + "<br />"
        rv += "density: " + str(planet.density) + "<br />"
        rv += "dust_mass: " + str(planet.dust_mass) + "<br />"
        rv += "e: " + str(planet.e) + "<br />"
        rv += "estimated_temp: " + str(planet.estimated_temp) + "<br />"
        rv += "estimated_terr_temp: " + str(planet.estimated_terr_temp) + "<br />"
        rv += "exospheric_temp: " + str(planet.exospheric_temp) + "<br />"
        rv += "gas_giant: " + str(planet.gas_giant) + "<br />"
        rv += "gas_mass: " + str(planet.gas_mass) + "<br />"
        rv += "greenhouse_effect: " + str(planet.greenhouse_effect) + "<br />"
        rv += "greenhs_rise: " + str(planet.greenhs_rise) + "<br />"
        rv += "high_temp: " + str(planet.high_temp) + "<br />"
        rv += "hydrosphere: " + str(planet.hydrosphere) + "<br />"
        rv += "ice_cover: " + str(planet.ice_cover) + "<br />"
        rv += "low_temp: " + str(planet.low_temp) + "<br />"
        rv += "mass: " + str(planet.mass) + "<br />"
        rv += "max_temp: " + str(planet.max_temp) + "<br />"
        rv += "min_temp: " + str(planet.min_temp) + "<br />"
        rv += "minor_moons: " + str(planet.minor_moons) + "<br />"
        rv += "molec_weight: " + str(planet.molec_weight) + "<br />"
        rv += "orb_period: " + str(planet.orb_period) + "<br />"
        rv += "resonant_period: " + str(planet.resonant_period) + "<br />"
        rv += "rms_velocity: " + str(planet.rms_velocity) + "<br />"
        rv += "surf_accel: " + str(planet.surf_accel) + "<br />"
        rv += "surf_pressure: " + str(planet.surf_pressure) + "<br />"
        rv += "surf_temp: " + str(planet.surf_temp) + "<br />"
        rv += "volatile_gas_inventory: " + str(planet.volatile_gas_inventory) + "<br />"

    return rv


def initializeDb():
    db.create_all()

    urlstars = urllib2.urlopen(uri + "/api2/?session=" + sid + "&command=longrange")
    urlstars = json.load(urlstars)

    for each in urlstars.values():
        for item in each:
            addition = Star(item)
            db.session.add(addition)

    db.session.commit()

def fillDbStarsystem():
    urlshort = urllib2.urlopen(uri + "/api2/?session=" + sid + "&command=shortrange")
    urlshort = json.load(urlshort)

    for each in urlshort.values():
        star = Star.query.filter_by(name=each["name"]).first()
        star = star.id
        for item in each["planetarray"]:
            addition = Planet(item, star)
            db.session.add(addition)

    db.session.commit()

def fillPlanetData():
    urlplanet = urllib2.urlopen(uri + "/api2/?session=" + sid + "&command=object")
    urlplanet = json.load(urlplanet)

    for each in urlplanet.values():
        if each:
            planet = Planet.query.filter_by(planet_no=each["planet_no"]).first()
            planet = planet.id
            addition = PlanDetails(each, planet)
            db.session.add(addition)
            print addition  
        else:
            return 0

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
    starid = db.Column(db.Integer)
    x = db.Column(db.Integer)
    y = db.Column(db.Integer)
    day = db.Column(db.Float)
    esc_velocity = db.Column(db.Float)
    cloud_cover = db.Column(db.Float)
    radius = db.Column(db.Float)
    planet_type = db.Column(db.String(50))
    planet_no = db.Column(db.String(50), unique=True)
    surf_grav = db.Column(db.Float)
    orbit_zone = db.Column(db.Integer)

    def __init__(self, dictionary, star):
        self.day = float(dictionary["day"])
        self.esc_velocity = float(dictionary["esc_velocity"])
        self.cloud_cover = float(dictionary["cloud_cover"])
        self.radius = float(dictionary["radius"])
        self.planet_type = str(dictionary["type"])
        self.planet_no = str(dictionary["planet_no"])
        self.x = int(dictionary["x"])
        self.surf_grav = float(dictionary["surf_grav"])
        self.y = int(dictionary["y"])
        self.orbit_zone = int(dictionary["orbit_zone"])
        self.starid = int(star)

class PlanDetails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    planetid = db.Column(db.Integer, unique=True)
    a = db.Column(db.Float)
    albedo = db.Column(db.Float)
    atmosphere = db.Column(db.String(50))
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
    gas_mass = db.Column(db.Float)
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

    def __init__(self, dictionary, planet):
        self.planetid = planet
        self.a = float(dictionary["a"])
        self.albedo = float(dictionary["albedo"])
        self.atmosphere = str(dictionary["atmosphere"])
        self.axial_tilt = float(dictionary["axial_tilt"])
        self.boil_point = float(dictionary["boil_point"])
        self.core_radius = float(dictionary["core_radius"])
        self.density = float(dictionary["density"])
        self.dust_mass = float(dictionary["dust_mass"])
        self.e = float(dictionary["e"])
        self.estimated_temp = float(dictionary["estimated_temp"])
        self.estimated_terr_temp = float(dictionary["estimated_terr_temp"])
        self.exospheric_temp = float(dictionary["exospheric_temp"])
        self.gas_giant = int(dictionary["gas_giant"])
        self.gas_mass = float(dictionary["gas_mass"])
        self.greenhouse_effect = int(dictionary["greenhouse_effect"])
        self.greenhs_rise = float(dictionary["greenhs_rise"])
        self.high_temp = float(dictionary["high_temp"])
        self.hydrosphere = float(dictionary["hydrosphere"])
        self.ice_cover = float(dictionary["ice_cover"])
        self.low_temp = float(dictionary["low_temp"])
        self.mass = float(dictionary["mass"])
        self.max_temp = float(dictionary["max_temp"])
        self.min_temp = float(dictionary["min_temp"])
        self.minor_moons = int(dictionary["minor_moons"])
        self.molec_weight = float(dictionary["molec_weight"])
        self.orb_period = float(dictionary["orb_period"])
        self.resonant_period = int(dictionary["resonant_period"])
        self.rms_velocity = float(dictionary["rms_velocity"])
        self.surf_accel = float(dictionary["surf_accel"])
        self.surf_pressure = float(dictionary["surf_pressure"])
        self.surf_temp = float(dictionary["surf_temp"])
        self.volatile_gas_inventory = float(dictionary["volatile_gas_inventory"])

def db2dict(db):
    d = []
    for row in db:
        c = {}
        for column in row.__table__.columns:
            c[column.name] = getattr(row, column.name)
        d.append(c)

    return d

if __name__ == "__main__":
    app.debug = True
    app.run()
