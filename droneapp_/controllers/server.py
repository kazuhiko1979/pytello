import logging

from flask import jsonify
from flask import render_template
from flask import request
from flask import Response

import droneapp_.models.course
from droneapp_.models.drone_manager import DroneManager

import config


logger = logging.getLogger(__name__)
app = config.app


def get_drone():
    return DroneManager()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/controller/')
def controller():
    return render_template('controller.html')


@app.route('/api/command/', methods=['POST'])
def command():
    cmd = request.form.get('command')
    logger.info({'action': 'command', 'cmd': cmd})
    drone = get_drone()
    if cmd == 'takeOff':
        drone.takeoff()
    if cmd == 'land':
        drone.land()
    if cmd == 'speed':
        speed = request.form.get('speed')
        logger.info({'action': 'command', 'cmd': cmd, 'speed': speed})
        if speed:
            drone.set_speed(int(speed))

    if cmd == 'up':
        drone.up()
    if cmd == 'down':
        drone.down()
    if cmd == 'forward':
        drone.forward()
    if cmd == 'back':
        drone.back()
    if cmd == 'clockwise':
        drone.clockwise()
    if cmd == 'counterClockwise':
        drone.counter_clockwise()
    if cmd == 'left':
        drone.left()
    if cmd == 'right':
        drone.right()
    if cmd == 'flipFront':
        drone.flip_front()
    if cmd == 'flipBack':
        drone.flip_back()
    if cmd == 'flipLeft':
        drone.flip_left()
    if cmd == 'flipRight':
        drone.flip_right()
    if cmd == 'patrol':
        drone.patrol()
    if cmd == 'stopPatrol':
        drone.stop_patrol()
    if cmd == 'faceDetectAndTrack':
        drone.enable_face_detect()
    if cmd == 'stopFaceDetectAndTrack':
        drone.disable_face_detect()
    if cmd == 'snapshot':
        if drone.snapshot():
            return jsonify(status='success'), 200
        else:
            return jsonify(status='fail'), 400

    return jsonify(status='success'), 200

def video_generator():
    drone = get_drone()
    for jpeg in drone.video_jpeg_generator():
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' +
               jpeg +
               b'\r\n\r\n')


@app.route('/video/streaming')
def video_feed():
    return Response(video_generator(), mimetype='multipart/x-mixed-replace; boundary=frame')

def get_courses(course_id=None):
    drone = get_drone()
    courses = droneapp_.models.course.get_courses(drone)
    if course_id:
        return courses.get(course_id)
    return courses


@app.route('/games/shake/')
def game_shake():
    courses = get_courses()
    return render_template('games/shake.html', courses=courses)


@app.route('/api/shake/start', methods=['GET', 'POST'])
def shake_start():
    # course_id = request.args.get('id')
    course_id = request.form.get('id')
    course = get_courses(int(course_id))
    course.start()
    return jsonify(result='started'), 200


@app.route('/api/shake/run', methods=['GET', 'POST'])
def shake_run():
    # course_id = request.args.get('id')
    course_id = request.form.get('id')
    course = get_courses(int(course_id))
    course.run()
    return jsonify(
        elapsed=course.elapsed,
        status=course.status,
        running=course.is_running), 200

def run():
    app.run(host=config.WEB_ADDRESS, port=config.WEB_PORT, threaded=True)
