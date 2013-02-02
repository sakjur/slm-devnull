from flask import Flask, render_template
import urllib2, urllib

app = Flask(__name__)
uri = "https://lostinspace.lanemarknad.se:8000"
sid = "f6319047-1cfb-4bfa-ae4b-318355d2b90e"

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
def currentSystem():
    urlshort = urllib2.urlopen(uri + "/api2/?session=" + sid + "&command=shortrange")
    short = urlshort.read()

    urlship = urllib2.urlopen(uri + "/api2/?session=" + sid + "&command=ship&arg=show")
    ship = urlship.read()

    return render_template('planetsystem.html', short=short, ship=ship)

if __name__ == "__main__":
    app.debug = True
    app.run()
