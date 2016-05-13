from flask import Flask, render_template, send_from_directory, Response
import subprocess
app = Flask(__name__, static_url_path='')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/jQuery-Flight-Indicators/<path:path>')
def send_js(path):
    return send_from_directory('jQuery-Flight-Indicators', path)


@app.route('/data/<path:path>')
def send_data(path):
    return send_from_directory('data', path)


if __name__ == '__main__':
    subprocess.Popen(['python', 'videoserver.py'])
    app.run(host='0.0.0.0', debug=False)
