from flask import Flask, render_template, send_from_directory, Response
from camera import VideoCamera

app = Flask(__name__, static_url_path='')


def gen(camera):
    while True:
        frame = camera.get_frame(1)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5001', debug=False)
