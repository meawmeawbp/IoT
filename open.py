import cv2

cap = cv2.VideoCapture(r'C:\miewmiew\Hackathon\IoT\checkcheck\output_cropped_angle.mp4')
fps = cap.get(cv2.CAP_PROP_FPS)
delay = int(1000 / fps)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    cv2.imshow('Frame', frame)
    if cv2.waitKey(delay) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
