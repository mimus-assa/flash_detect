#Import necessary libraries
from flask import Flask, render_template, Response
import cv2
import imageio
import numpy as np
from flask_mail import Mail, Message


#Initialize the Flask app
app = Flask(__name__)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'xxxxxxx@gmail.com'
app.config['MAIL_PASSWORD'] = "xxxxxxx"
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

stream = "rtsp://root:toor@xxx.xxx.xxx.xxx/"
camera = cv2.VideoCapture(stream)
YEYE = ["none"]

def send_mail_ohyea(y,Y):
    mail_list = ['xxx']
    for i in mail_list:
        if y != Y[-1] and Y[-1]=="none":
            #print("cambio!",y,Y[-1])
            msg = Message('Planta de medina', sender = 'xxxx@gmail.com', recipients = [i])
            msg.body = "se inicia el monitoreo"
            mail.send(msg)
        if y != Y[-1] and y =="light" and Y[-1]=="dark":
            #print("cambio!",y,Y[-1])
            msg = Message('Planta de medina', sender = 'xxxx@gmail.com', recipients = [i])
            msg.body = "la luz se encendio"
            mail.send(msg)
        if y != Y[-1] and y =="dark" and Y[-1]=="light":
            #print("cambio!",y,Y[-1])
            msg = Message('Planta de medina', sender = 'xxxx@gmail.com', recipients = [i])
            msg.body = "la luz se apago"
            mail.send(msg)

def img_estim(night, cam):
    
    is_light = np.mean(cam) > np.mean(night)+20
    return 'light' if is_light else 'dark'
    
def gen_frames():  
    while True:
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            
            filename_noche = "xxxxxxxxxxxxxxx"
            noche = imageio.imread(filename_noche, as_gray=True)
            ret, buffer = cv2.imencode('.jpg', frame)
            y = img_estim(noche, frame)
            with app.app_context():
                send_mail_ohyea(y,YEYE)
            YEYE.append(img_estim(noche, frame))
            frame = buffer.tobytes()
           
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True)
