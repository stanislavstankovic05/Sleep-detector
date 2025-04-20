import cv2
import tensorflow as tf
import numpy as np

model = tf.keras.models.load_model('final_model.keras')

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Can't open camera")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("error, can't receive frame")
        break

    frame = cv2.flip(frame, 1)
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.3, minNeighbors=5)

    for (face_x, face_y, face_width, face_height) in faces:

        face_roi_gray = gray_frame[face_y:face_y+face_height, face_x:face_x+face_width]
        face_roi_color = frame[face_y:face_y+face_height, face_x:face_x+face_width]
        eyes = eye_cascade.detectMultiScale(face_roi_gray)

        for (eye_x, eye_y, eye_width, eye_height) in eyes:
            eye_gray = face_roi_gray[eye_y:eye_y+eye_height, eye_x:eye_x+eye_width]

            eye_resized = cv2.resize(eye_gray, (128, 128))
            eye_normalized = eye_resized / 255.0

            eye_input = np.expand_dims(eye_normalized, axis=-1)
            eye_input = np.expand_dims(eye_input, axis=0)

            prediction = model.predict(eye_input)[0][0]
            if prediction < 0.5:
                label = "Awake"
                confidence = 1 - prediction
                color = (0, 255, 0) #green
            else:
                label = "Sleepy"
                confidence = prediction
                color = (0, 0, 255) #red

            cv2.rectangle(face_roi_color, (eye_x, eye_y), (eye_x+eye_width, eye_y+eye_height), color, 2)
            cv2.putText(face_roi_color, f"{label}", (eye_x, eye_y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    cv2.imshow("Eye Test", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
