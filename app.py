# from flask import Flask, render_template, redirect, url_for, request
# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# import threading
# import torch
# import cv2

# app = Flask(__name__)

# # Mail configuration
# def send_proctoring_alert():
#     sender_email = "anushree.deshapande1999@gmail.com"  # Your email
#     receiver_email = "saroja.deshapande99@gmail.com"    # Receiver's email
#     password = "xyfc mdwo xlwu ynpp"  # Your Gmail App Password (ensure this is correct and not your Gmail password)
    
#     msg = MIMEMultipart()
#     msg['From'] = sender_email
#     msg['To'] = receiver_email
#     msg['Subject'] = "Proctoring Alert"
    
#     body = body = """
#     Suspicious activity detected (mobile phone).
#     Proctoring alert: A mobile phone has been detected.
#     Please review the situation and take necessary action.
#     Mobile phones during exams are strictly prohibited.
#     This is an automated alert from the exam proctoring system.
#     """
#     msg.attach(MIMEText(body, 'plain'))
    
#     try:
#         # Connect to Gmail SMTP server
#         server = smtplib.SMTP('smtp.gmail.com', 587)
#         server.starttls()  # Secure the connection
#         server.login(sender_email, password)  # Use your app password here
#         text = msg.as_string()
#         server.sendmail(sender_email, receiver_email, text)  # Send the email
#         server.quit()  # Close the connection
#         print("Proctoring alert email sent successfully.")
#     except smtplib.SMTPException as e:
#         print(f"Error sending email: {e}")

# # Load YOLOv5 model
# model = torch.hub.load('ultralytics/yolov5', 'yolov5s')  # Use the pre-trained YOLOv5 small model

# # Global variable to control webcam thread
# webcam_active = False

# # Webcam detection function (simulated for mobile detection)
# def check_for_mobile():
#     global webcam_active
#     # Open webcam
#     cap = cv2.VideoCapture(0)
#     while cap.isOpened() and webcam_active:
#         ret, frame = cap.read()
#         if not ret:
#             break
        
#         # Perform object detection using YOLOv5
#         results = model(frame)  # Get detections from the model
#         labels = results.names  # Get labels from the model

#         # Loop through detected objects and check if any are a mobile phone
#         detected_objects = results.xywh[0][:, -1].cpu().numpy()  # Get detected class IDs
#         for obj in detected_objects:
#             if labels[int(obj)] == 'cell phone':  # Check if a 'cell phone' is detected
#                 print("Suspicious activity detected (mobile phone).")
#                 send_proctoring_alert()
#                 break  # Stop after detecting mobile phone
        
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break

#     cap.release()

# # Function to start the webcam in a separate thread
# def start_webcam():
#     global webcam_active
#     webcam_active = True
#     check_for_mobile()

# @app.route('/')
# def home():
#     return render_template('start.html')

# @app.route('/exam')
# def exam():
#     # Start the webcam in the background when the exam starts
#     threading.Thread(target=start_webcam, daemon=True).start()
#     return render_template('exam.html')

# @app.route('/submit_exam', methods=['POST'])
# def submit_exam():
#     # Example logic for checking answers
#     score = 0
#     correct_answers = {
#         'q1': 'Paris',
#         'q2': 'JavaScript',
#         'q3': 'HyperText Markup Language',
#         'q4': 'Mitochondria',
#         'q5': '100°C',
#         'q6': 'Albert Einstein',
#         'q7': 'Jupiter',
#         'q8': 'Oxygen',
#         'q9': 'Microsoft',
#         'q10': '299,792 km/s'
#     }
    
#     for question, correct_answer in correct_answers.items():
#         if request.form.get(question) == correct_answer:
#             score += 1

#     # Stop webcam and monitoring after exam submission
#     global webcam_active
#     webcam_active = False  # This will stop the webcam thread

#     return redirect(url_for('result', score=score))

# @app.route('/result')
# def result():
#     score = request.args.get('score')
#     return render_template('result.html', score=score)

# if __name__ == '__main__':
#     # Specify the host and port (example: host='0.0.0.0', port=5000)
#     app.run(debug=True, host='0.0.0.0', port=5000)

import cv2
from flask import Flask, render_template, redirect, url_for, request, Response
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import threading
import torch

app = Flask(__name__)

# Mail configuration
def send_proctoring_alert():
    sender_email = "anushree.deshapande1999@gmail.com"  # Your email
    receiver_email = "saroja.deshapande99@gmail.com"    # Receiver's email
    password = "xyfc mdwo xlwu ynpp"  # Your Gmail App Password (ensure this is correct and not your Gmail password)
    
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = "Proctoring Alert"
    
    body = """
    Suspicious activity detected (mobile phone).
    Proctoring alert: A mobile phone has been detected.
    Please review the situation and take necessary action.
    Mobile phones during exams are strictly prohibited.
    This is an automated alert from the exam proctoring system.
    """
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        # Connect to Gmail SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # Secure the connection
        server.login(sender_email, password)  # Use your app password here
        text = msg.as_string()
        server.sendmail(sender_email, receiver_email, text)  # Send the email
        server.quit()  # Close the connection
        print("Proctoring alert email sent successfully.")
    except smtplib.SMTPException as e:
        print(f"Error sending email: {e}")

# Load YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')  # Use the pre-trained YOLOv5 small model

# Global variable to control webcam thread
webcam_active = False

# Webcam detection function (simulated for mobile detection)
def check_for_mobile():
    global webcam_active
    # Open webcam
    cap = cv2.VideoCapture(0)
    while cap.isOpened() and webcam_active:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Perform object detection using YOLOv5
        results = model(frame)  # Get detections from the model
        labels = results.names  # Get labels from the model

        # Loop through detected objects and check if any are a mobile phone
        detected_objects = results.xywh[0][:, -1].cpu().numpy()  # Get detected class IDs
        for obj in detected_objects:
            if labels[int(obj)] == 'cell phone':  # Check if a 'cell phone' is detected
                print("Suspicious activity detected (mobile phone).")
                send_proctoring_alert()
                break  # Stop after detecting mobile phone
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()

# Function to start the webcam in a separate thread
def start_webcam():
    global webcam_active
    webcam_active = True
    check_for_mobile()

# Webcam feed generator function
def gen():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        ret, jpeg = cv2.imencode('.jpg', frame)
        if ret:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')

    cap.release()

# Route to serve the video feed
@app.route('/video_feed')
def video_feed():
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def home():
    return render_template('start.html')

@app.route('/exam')
def exam():
    # Start the webcam in the background when the exam starts
    threading.Thread(target=start_webcam, daemon=True).start()
    return render_template('exam.html')

@app.route('/submit_exam', methods=['POST'])
def submit_exam():
    # Example logic for checking answers
    score = 0
    correct_answers = {
        'q1': 'Paris',
        'q2': 'JavaScript',
        'q3': 'HyperText Markup Language',
        'q4': 'Mitochondria',
        'q5': '100°C',
        'q6': 'Albert Einstein',
        'q7': 'Jupiter',
        'q8': 'Oxygen',
        'q9': 'Microsoft',
        'q10': '299,792 km/s'
    }
    
    for question, correct_answer in correct_answers.items():
        if request.form.get(question) == correct_answer:
            score += 1

    # Stop webcam and monitoring after exam submission
    global webcam_active
    webcam_active = False  # This will stop the webcam thread

    return redirect(url_for('result', score=score))

@app.route('/result')
def result():
    score = request.args.get('score')
    return render_template('result.html', score=score)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)












