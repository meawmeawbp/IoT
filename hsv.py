import cv2
import numpy as np

def nothing(x):
    pass

# โหลดวิดีโอ
cap = cv2.VideoCapture(r'C:\miewmiew\Hackathon\IoT\checkcheck\clip2.mp4')  # 👉 ใส่ path วิดีโอของคุณ!

# ตั้งค่าบันทึกวิดีโอ
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('hsv_output2.mp4', fourcc, 30, 
                      (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))

# สร้าง Trackbars
cv2.namedWindow('Trackbars')
cv2.createTrackbar('LH', 'Trackbars', 0, 180, nothing)
cv2.createTrackbar('LS', 'Trackbars', 0, 255, nothing)
cv2.createTrackbar('LV', 'Trackbars', 0, 255, nothing)
cv2.createTrackbar('UH', 'Trackbars', 180, 180, nothing)
cv2.createTrackbar('US', 'Trackbars', 255, 255, nothing)
cv2.createTrackbar('UV', 'Trackbars', 255, 255, nothing)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # แปลงเป็น HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # อ่านค่า Trackbars
    l_h = cv2.getTrackbarPos('LH', 'Trackbars')
    l_s = cv2.getTrackbarPos('LS', 'Trackbars')
    l_v = cv2.getTrackbarPos('LV', 'Trackbars')
    u_h = cv2.getTrackbarPos('UH', 'Trackbars')
    u_s = cv2.getTrackbarPos('US', 'Trackbars')
    u_v = cv2.getTrackbarPos('UV', 'Trackbars')

    # สร้าง mask
    lower = np.array([l_h, l_s, l_v])
    upper = np.array([u_h, u_s, u_v])
    mask = cv2.inRange(hsv, lower, upper)

    # ผลลัพธ์การกรอง
    result = cv2.bitwise_and(frame, frame, mask=mask)

    # Optional: วาด contour/เส้นแบ่งน้ำเงินด้วย HoughLinesP
    edges = cv2.Canny(mask, 50, 150, apertureSize=3)
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=50, minLineLength=30, maxLineGap=10)
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(result, (x1, y1), (x2, y2), (0, 0, 255), 2)

    # แสดงผล
    cv2.imshow('Original', frame)
    cv2.imshow('Mask', mask)
    cv2.imshow('Result', result)

    # บันทึกวิดีโอ
    out.write(result)

    # กด ESC (27) เพื่อออก
    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
out.release()
cv2.destroyAllWindows()
