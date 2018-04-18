from flask import Flask
from flask import render_template
from flask_socketio import SocketIO, emit
from PIL import Image
import base64
from io import BytesIO
import emotionDetector
import numpy as np

app = Flask(__name__)
app.config['SECRET_KEU'] = 'secret!'
socketio = SocketIO(app)
emotions = ["ANGRY", "HAPPY", "SAD", "ABSOLUTELY DISGUSTED", "FEARFUL","NEUTRAL","SURPRISED"]  # Emotion list


@app.route("/")
def index():
    return render_template("vid.html")


@socketio.on('vid_frame', namespace='/vid')
def receive_frame(message):
    import base64
    base64_image_str = message['imageData'][message['imageData'].find(",") + 1:]
    im = Image.open(BytesIO(base64.b64decode(base64_image_str)))
    rgb_im = np.array(im)  # 640x480x4 array
    #rgb_im[20, 30]
    #rgb_im.reshape(1, -1)
    if emotionDetector.isClassifierTrained():
        prediction = emotionDetector.predict(rgb_im)
        if prediction is not None:
            print(emotions[prediction[0]])
            emotion = emotions[prediction[0]]
            emit('Emotion', {'emotion': emotion})
    else:
        emit('Emotion', {'emotion': "Working... " + str(emotionDetector.current_cv+1) + " of "
                                    + str(emotionDetector.CVs)})


@socketio.on('connect', namespace='/vid')
def test_connect():
    print("test_connect")
    if not emotionDetector.isClassifierTrained():
        emotionDetector.build_clf()
    emit('my response', {'data': 'Connected'})


@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')


@app.route("/vf")
def video_feed():
    return render_template("vid.html")


if __name__ == "__main__":
    #app.run(host='0.0.0.0',debug=False, port=5000)
    #app.run(debug=True)
    app.config.update(TEMPLATES_AUTO_RELOAD=True)
    socketio.run(app)#, host='0.0.0.0', port=5000)
