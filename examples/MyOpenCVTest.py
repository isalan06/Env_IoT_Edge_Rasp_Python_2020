import cv2

cap = cv2.VideoCapture(0)
cap.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 800)
cap.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 600)

while True:
    ret, frame = cap.read()
    cv2.imshow("preview", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
       
cap.release()
cv2.destroyAllWindows()