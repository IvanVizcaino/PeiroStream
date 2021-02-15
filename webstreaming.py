# USAGE
# python webstreaming.py --ip 0.0.0.0 --port 8000

# import the necessary packages
from flask import Response
from flask import Flask
from flask import render_template
from flask import request
import os
import threading
import argparse
import datetime
import time
import numpy as np
from flask import request
from flask import jsonify
from subprocess import call
import pylivestream.api as pls
import find_process as process
# initialize the output frame and a lock used to ensure thread-safe
# exchanges of the output frames (useful for multiple browsers/tabs
# are viewing tthe stream)
outputFrame = None
lock = threading.Lock()
resolution_width = 1280

# initialize a flask object
app = Flask(__name__)
status = "live"

@app.route("/", methods=['GET', 'POST'])
def index():
    try:
        global status
        error = None
    except:
        error = "No pudimos conectar con la cámara"
    # return the rendered template
    return render_template("index.html", base_url=request.base_url, cameras=[0, 1], errors=error, status=status)

@app.route("/youtube", methods=['GET', 'POST'])
def youtube():
    return render_template("youtube.html",status=status)


@app.route("/settings", methods=['GET', 'POST'])
def settings():
    return render_template("settings.html", resolution_width=resolution_width, status=status)


@app.route("/shutdown")
def shutdown():
    call("sudo shutdown -h now", shell=True)

def localStreaming():
    pls.stream_webcam(ini_file="/home/pi/.local/lib/python3.7/site-packages/pylivestream/pylivestream.ini", websites="localhost", assume_yes=True, timeout=360000)

@app.route("/stop")
def stopStreaming():
    listOfProcessIds = process.findProcessIdByName('ffmpeg')
    try:
        if len(listOfProcessIds) > 0:
            for elem in listOfProcessIds:
                call("sudo kill " + elem['pid'], shell=True)
                #os.kill(elem['pid'], signal.SIGKILL)
    except:
        return jsonify(
            result=False,
        )
    return jsonify(
            result=True,
        )

# check to see if this is the main thread of execution
if __name__ == '__main__':
    # construct the argument parser and parse command line arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--ip", type=str, required=True,
                    help="ip address of the device")
    ap.add_argument("-o", "--port", type=int, required=True,
                    help="ephemeral port number of the server (1024 to 65535)")
    ap.add_argument("-f", "--frame-count", type=int, default=32,
                    help="# of frames used to construct the background model")
    args = vars(ap.parse_args())

    # start a thread that will perform motion detection
    try:
        t = threading.Thread(target=localStreaming)
        t.daemon = True
        t.start()
    except:
        status = "offline"
    
    
    # start the flask app
    app.run(host=args["ip"], port=args["port"], debug=True,
            threaded=True, use_reloader=False)

