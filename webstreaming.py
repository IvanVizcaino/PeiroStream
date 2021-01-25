# USAGE
# python webstreaming.py --ip 0.0.0.0 --port 8000

# import the necessary packages
from pyimagesearch.motion_detection import SingleMotionDetector
from imutils.video import VideoStream
from flask import Response
from flask import Flask
from flask import render_template
from flask import request
import threading
import argparse
import datetime
import imutils
import time
import cv2
import numpy as np
from flask import request
from subprocess import call


# initialize the output frame and a lock used to ensure thread-safe
# exchanges of the output frames (useful for multiple browsers/tabs
# are viewing tthe stream)
outputFrame = None
lock = threading.Lock()
resolution_width = 1280

# initialize a flask object
app = Flask(__name__)

# initialize the video stream and allow the camera sensor to
# warmup
#vs = VideoStream(usePiCamera=1).start()
vs = VideoStream(src=0).start()
time.sleep(2.0)


@app.route("/", methods=['GET', 'POST'])
def index():
    try:
        global vs, resolution_width
        error = None
        if request.args.get('resolution') is not None:
            resolution_width = int(request.args.get('resolution'))
        if request.args.get('camera') is not None:
            vs.stop()
            vs = VideoStream(src=int(request.args.get('camera'))).start()
            time.sleep(2.0)
    except:
        error = "No pudimos conectar con la cámara"
    # return the rendered template
    return render_template("index.html", base_url=request.base_url, cameras=[0, 1], errors=error)


def stream(frameCount):
    # grab global references to the video stream, output frame, and
    # lock variables
    global vs, outputFrame, lock, resolution_width

    # loop over frames from the video stream
    while True:
        # read the next frame from the video stream, resize it,
        # convert the frame to grayscale, and blur it
        try:
            frame = vs.read()
            frame = imutils.resize(frame, width=resolution_width)
            #frame = cv2.fastNlMeansDenoisingColored(frame,None,10,10,7,21)
        except:
            frame = np.zeros((400, 400, 3), np.uint8)

            font = cv2.FONT_HERSHEY_SIMPLEX
            bottomLeftCornerOfText = (100, 200)
            fontScale = 2
            fontColor = (255, 255, 255)
            lineType = 2

            cv2.putText(frame, 'Error',
                        bottomLeftCornerOfText,
                        font,
                        fontScale,
                        fontColor,
                        lineType)

        # acquire the lock, set the output frame, and release the
        # lock
        with lock:
            outputFrame = frame.copy()


def generate():
    # grab global references to the output frame and lock variables
    global outputFrame, lock

    # loop over frames from the output stream
    while True:
        # wait until the lock is acquired
        with lock:
            # check if the output frame is available, otherwise skip
            # the iteration of the loop
            if outputFrame is None:
                continue

            # encode the frame in JPEG format
            (flag, encodedImage) = cv2.imencode(".jpg", outputFrame)

            # ensure the frame was successfully encoded
            if not flag:
                continue

        # yield the output frame in the byte format
        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
              bytearray(encodedImage) + b'\r\n')


@app.route("/video_feed")
def video_feed():
    # return the response generated along with the specific media
    # type (mime type)
    return Response(generate(),
                    mimetype="multipart/x-mixed-replace; boundary=frame")


@app.route("/youtube", methods=['GET', 'POST'])
def youtube():
    return render_template("youtube.html")


@app.route("/settings", methods=['GET', 'POST'])
def settings():
    return render_template("settings.html", resolution_width=resolution_width)


@app.route("/shutdown")
def shutdown():
    call("sudo shutdown -h now", shell=True)


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
    t = threading.Thread(target=stream, args=(
        args["frame_count"],))
    t.daemon = True
    t.start()

    # start the flask app
    app.run(host=args["ip"], port=args["port"], debug=True,
            threaded=True, use_reloader=False)

# release the video stream pointer
vs.stop()
