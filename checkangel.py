import cv2
import numpy as np

# โหลดวิดีโอ
video_path = "/mnt/data/Untitled video - Made with Clipchamp.mp4"
cap = cv2.VideoCapture(video_path)

# ตั้งค่าการบันทึกวิดีโอผลลัพธ์ (Optional)
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('output_with_angles.mp4', fourcc, 30, 
                      (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))

prev_angle = None  # เก็บมุมเฟรมก่อนหน้า
frame_count = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_count += 1

    # แปลงเป็น grayscale + blur + threshold
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 100, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # หา contour
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    angle = None

    if contours:
        c = max(contours, key=cv2.contourArea)
        if len(c) >= 5:
            ellipse = cv2.fitEllipse(c)
            angle = ellipse[2]  # มุมของทุ่น

            # วาด ellipse บนเฟรม
            cv2.ellipse(frame, ellipse, (0, 255, 0), 2)

    # คำนวณ delta angle
    if angle is not None and prev_angle is not None:
        # ปรับค่า delta ให้อยู่ในช่วง -180 ถึง 180
        delta_angle = (angle - prev_angle + 180) % 360 - 180
        text = f"Angle: {angle:.2f} deg | Delta: {delta_angle:.2f} deg"
    else:
        text = f"Angle: {angle:.2f} deg" if angle is not None else "Angle: None"

    # แสดงข้อความบนวิดีโอ
    cv2.putText(frame, text, (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # แสดงผลเฟรม
    cv2.imshow('Rotation Tracking', frame)

    # บันทึกวิดีโอผลลัพธ์
    out.write(frame)

    # เก็บมุมปัจจุบันเพื่อเทียบในรอบถัดไป
    if angle is not None:
        prev_angle = angle

    # กด q เพื่อออก
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# ปิด
cap.release()
out.release()
cv2.destroyAllWindows()
print("Done!")
