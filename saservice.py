import json
import logging
import os
import uuid
import click

from threading import Event
from threading import Lock
from threading import Thread

from flask import Flask
from flask import jsonify
from flask import request

from common.configpolicies import PolicyConfigs
from common.configurls import URLConfigs
import common
from situationalawareness.awareness import SituationalAwareness
from situationalawareness.compliance.impulsepolicy import ImpulsePolicy
from situationalawareness.compliance.policies import Policies
from situationalawareness.compliance.windowpolicy import WindowPolicy
from situationalawareness.comprehensionstage import TCONST
from common.configurls import URLConfigs

app = Flask(__name__)
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

thread = Thread()
lock = Lock()
stopEvent = Event()

impulsePolicy = ImpulsePolicy(PolicyConfigs.IMPULSE_POLICY)
windowPolicies = set()
for wconfig in PolicyConfigs.WINDOW_POLICIES:
    windowPolicies.add(WindowPolicy(wconfig[0], wconfig[1]))


@app.route("/getTracker/<string:id>")
def getTracker(id):

    policyUUID = uuid.UUID(id)
    out = jsonify({'Exception': 'Tracker '+id+' could not be found'})
    situation = thread.getComprehension().getSituation()
    lock.acquire()
    try:
        if situation.containsTracker(policyUUID):
            out = situation.getTracker(policyUUID).toJSON()
    finally:
        lock.release()
        return out

@app.route("/removeWindowPolicy/<string:id>")
def removeWindowPolicy(id):
    result = False
    policyUUID = uuid.UUID(id)
    result = thread.removeWindowPolicy(policyUUID)
    return jsonify(Result=result)

@app.route("/addWindowPolicy", methods = ['POST'])
def addWindowPolicy():
    j = request.get_json()
    content = json.loads(j)
    thres = content[TCONST.NOISE_THRES]
    size = content[TCONST.WIN_SIZE]
    newPolicy = WindowPolicy(thres, size)
    thread.getPolicies().addWindowPolicy(newPolicy)
    return jsonify(newPolicy.toDict())

@app.route("/getBrokenPolicies")
def getBrokenPolicies():
    return jsonify({'policies': thread.getBrokenPolicies()})

@app.route("/getBrokenPolicyTrackers/<string:id>")
def getBrokenPolicyTrackers(id):
    policyUUID = uuid.UUID(id)
    return jsonify({'trackers': thread.getBrokenPolicy(policyUUID)})

@app.route("/getPolicies")
def getPolicies():
    return thread.getPolicies().toJSON()

@app.route("/getPolicy/<string:id>")
def getPolicy(id):
    policyUUID = uuid.UUID(id)
    return thread.getPolicies().policyAsJSON(policyUUID)

@app.route('/shutdown', methods = ['POST'])
def shutdown():
    shutdownAwareness()
    return shutdownFlask()

def shutdownAwareness():
    # shutdown situational awareness thread
    try:
        if(thread.is_alive()):
            stopEvent.set()
            thread.join()
        else:
            raise Exception("Issue occured while shutting down situational awareness thread")
    except Exception as exception:
        print(exception)

def shutdownFlask():
    msg = "Service Not Shutdown Successfully"
    unsuccessful = True

    #shutdown flask server
    try:
        func = request.environ.get('werkzeug.server.shutdown')
        if func is not None:
            func()
            msg = "Service Shutdown Successfully"
            unsuccessful = False
        return msg
    finally:
        if unsuccessful:
            raise RuntimeError('Not running with the Werkzeug Server')


def clearScreen():
    os.system('clear')
    os.system("printf '\e[3J'")

@click.command()
@click.option('--sahost', envvar="SAHOST")
@click.option('--michost', envvar="MICHOST")
@click.option('--gpshost', envvar="GPSHOST")
@click.option('--saport', envvar="SAPORT")
@click.option('--micport', envvar="MICPORT")
@click.option('--gpsport', envvar="GPSPORT")
def main(sahost, michost, gpshost, saport, micport, gpsport):

#todo working on setting host command line arguments so containers will be able to call eachother on horizon generated docker network between containers

    for param in os.environ.keys():
        if 'HOST' in param:
            print ("%20s %s" % (param, os.environ[param]))

    if(sahost is not None):
        common.sahost = sahost

    if (michost is not None):
       common.michost = michost

    if (gpshost is not None):
        common.gpshost = gpshost

    if(saport is not None):
        common.saport = saport

    if (micport is not None):
       common.micport = micport

    if (gpsport is not None):
        common.gpsport = gpsport

    urls = URLConfigs(common.michost, common.gpshost, common.sahost)
    click.echo("{}, {}, {}".format(sahost, common.sahost, urls.SA_HOST))
    click.echo("{}, {}, {}".format(michost, common.michost, urls.MIC_HOST))
    click.echo("{}, {}, {}".format(gpshost, common.gpshost, urls.GPS_HOST))


    global thread
    if not thread.isAlive():
        thread = SituationalAwareness(stopEvent, lock, Policies(impulsePolicy, windowPolicies), urls)
        thread.start()

    app.run(common.listeningIP, common.saport)

if __name__ == "__main__":
    main()

