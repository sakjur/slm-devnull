from flask import Flask, render_template
import urllib2

app = Flask(__name__)

@app.route("/")
def hello():
    url = urllib2.urlopen("https://lostinspace.lanemarknad.se:8000/api2/?session=f6319047-1cfb-4bfa-ae4b-318355d2b90e&command=longrange")
    stars = url.read().decode('utf-8')

    return render_template('starsystem.html', stars=stars)

if __name__ == "__main__":
    app.debug = True
    app.run()
