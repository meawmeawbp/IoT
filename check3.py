import cv2
import numpy as np
import math
import pandas as pd

# โหลดวิดีโอ
cap = cv2.VideoCapture(r'C:\miewmiew\Hackathon\IoT\checkcheck\clip2.mp4')

# ดึง FPS
fps = cap.get(cv2.CAP_PROP_FPS)
delay = int(1000 / fps)

frame_count = 0
baseline_angle = None
angles = []

# ตั้งค่าการบันทึกวิดีโอ
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('output_buoy_angle_all_frames.mp4', fourcc, fps,
                      (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame_count += 1

    # แปลงเป็น grayscale + threshold
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

    # หา Contour ใหญ่สุด
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    angle_to_show = None

    if contours:
        c = max(contours, key=cv2.contourArea)

        if len(c) >= 5:
            ellipse = cv2.fitEllipse(c)
            angle = ellipse[2] % 360  # มุม 0–360

            if baseline_angle is None:
                baseline_angle = angle

            # มุม relative
            relative_angle = (angle - baseline_angle + 360) % 360
            angles.append(relative_angle)
            angle_to_show = relative_angle

            # Overlay ellipse + มุม
            cv2.ellipse(frame, ellipse, (0, 255, 0), 2)
        else:
            angles.append(None)
    else:
        angles.append(None)

    # Overlay มุมอย่างชัดเจน
    if angle_to_show is not None:
        cv2.putText(frame, f"Angle: {angle_to_show:.2f} deg", (10, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)
    else:
        cv2.putText(frame, "Angle: None", (10, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)

    # บันทึกวิดีโอ
    out.write(frame)

    # แสดงผล
    cv2.imshow('Frame', frame)
    if cv2.waitKey(delay) & 0xFF == ord('q'):
        break

cap.release()
out.release()
cv2.destroyAllWindows()

# บันทึก CSV
df = pd.DataFrame({
    'frame': range(1, len(angles) + 1),
    'relative_angle': angles
})
df.to_csv('buoy_angle_all_frames.csv', index=False)

print("✅ เสร็จแล้ว! output_buoy_angle_all_frames.mp4 + buoy_angle_all_frames.csv (มี overlay ชัดเจนแล้ว!)")
