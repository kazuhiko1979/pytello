import cv2 as cv

cap = cv.VideoCapture(0)

face_cascade = cv.CascadeClassifier(r".\tools\haarcascade_frontalface_default.xml")
eyes_cascade = cv.CascadeClassifier(r".\tools\haarcascade_eye.xml")

while True:
    ret, frame = cap.read()
    # frame = cv.imread(r".\tools\image.jpg")

    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    print(len(faces))

    for (x, y, w, h) in faces:
        cv.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        eye_gray = gray[y:y+h, x:x+w]
        eye_color = frame[y:y+h, x:x+w]
        eyes = eyes_cascade.detectMultiScale(eye_gray)
        for (ex, ey, ew, eh) in eyes:
            cv.rectangle(eye_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)

    cv.imshow('frame', frame)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cv.destroyAllWindows()




















