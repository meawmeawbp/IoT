import cv2
import numpy as np

def get_rotation_angle(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        c = max(contours, key=cv2.contourArea)
        if len(c) >= 5:
            ellipse = cv2.fitEllipse(c)
            angle = ellipse[2] % 360
            return angle
    return None

# ใส่ path ภาพ 2 รูปที่ crop แล้ว
img1_path = r'C:\miewmiew\Hackathon\IoT\checkcheck\random_crops\crop_001.jpg'
img2_path = r'C:\miewmiew\Hackathon\IoT\checkcheck\random_crops\crop_002.jpg'

angle1 = get_rotation_angle(img1_path)
angle2 = get_rotation_angle(img2_path)

if angle1 is not None and angle2 is not None:
    diff_angle = abs(angle2 - angle1)
    print(f"มุมภาพ 1: {angle1:.2f}°")
    print(f"มุมภาพ 2: {angle2:.2f}°")
    print(f"มุมที่ต่างกัน: {diff_angle:.2f}°")
else:
    print("หา ellipse ไม่เจอในภาพหนึ่งภาพใด")
