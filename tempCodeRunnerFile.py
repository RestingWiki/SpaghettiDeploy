from roboflow import Roboflow
from flask import Flask, render_template, Response
import cv2

app = Flask(__name__)

# Test detection, change the api_key and the project later
def generate_frames():
    rf = Roboflow(api_key="Lla4Lh0uVbvsXBCBV6Go")
    project = rf.workspace().project("face-detection-mik1i")
    model = project.version(21).model

    # Open video capture from the webcam
    cap = cv2.VideoCapture(0)

    while True:
        # Read a frame from the video source
        ret, frame = cap.read()

        if not ret:
            break

        # Perform inference on the frame
        predictions = model.predict(frame, confidence=40, overlap=30).json()
        print (predictions)
        # Process the predictions and draw bounding boxes on the frame
        for prediction in predictions['predictions']:
            cx = int(prediction['x'])
            cy = int(prediction['y'])
            w = int(prediction['width'])
            h = int(prediction['height'])

            # Calculate the coordinates of the top-left and bottom-right corners
            x1 = cx - w // 2
            y1 = cy - h // 2
            x2 = cx + w // 2
            y2 = cy + h // 2

            # Draw the rectangle on the frame
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

        # Convert the frame to JPEG format
        ret, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()

        # Yield the frame as a response to the client
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    # Release the video capture and cleanup
    cap.release()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
