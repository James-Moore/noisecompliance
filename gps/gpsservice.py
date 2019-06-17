from flask import Flask
from flask import request
from gps.ipgps import IpGPS
import logging
import common
import click

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
gps = IpGPS()
app = Flask(__name__)

@app.route('/getLongitude')
def getLongitude():
    return gps.longitudeAsJSON()

@app.route('/getLatitude')
def getLatitude():
    return gps.latitudeAsJSON()

@app.route('/getCoordinates')
def getCoordinates():
    return gps.toJSON()

@app.route('/shutdown', methods = ['POST'])
def shutdown():
    msg = "Service Not Shutdown Successfully"
    unsuccessful = True

    try:
        func = request.environ.get('werkzeug.server.shutdown')
        if func is not None:
            func()
            msg = "Service Shutdown Successfully"
            unsuccessful = False
        print(msg)
        return msg
    finally:
        if unsuccessful:
            raise RuntimeError('Not running with the Werkzeug Server')



@click.command()
@click.option('--gpsport', envvar="GPSPORT")
def main(gpsport):

    if (gpsport is not None):
        common.gpsport = gpsport

    app.run(common.listeningIP, common.gpsport)

if __name__ == '__main__':
    main()