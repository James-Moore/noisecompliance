import logging
import click

from flask import Flask, request

import common
from microphone.mic import Microphone

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__)


@app.route('/getDecible')
def getDecible():
    mic = Microphone()
    return  str(mic.getDecible())

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
@click.option('--micport', envvar="MICPORT")
def main(micport):

    if (micport is not None):
       common.micport = micport

    app.run(common.listeningIP, common.micport)

if __name__ == '__main__':
    main()