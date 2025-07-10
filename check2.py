import cv2
import numpy as np
import math

# โหลดวิดีโอ
video_path = r'C:\miewmiew\Hackathon\IoT\checkcheck\hsv_output2.mp4'
cap = cv2.VideoCapture(video_path)

# ดึง FPS จริงของวิดีโอ
fps = cap.get(cv2.CAP_PROP_FPS)
delay = int(1000 / fps)
frames_per_3sec = int(fps * 3)

# ตั้งค่าการบันทึกวิดีโอ
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('output_detect_blue_line.mp4', fourcc, fps, 
                      (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))

# เก็บมุมที่ตรวจจับได้
angles = []
frame_count = 0
baseline_angle = None

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame_count += 1


    # แปลงเป็น HSV + Mask สีฟ้า
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_blue = np.array([90, 50, 50])
    upper_blue = np.array([130, 255, 255])
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # ขยายเส้นด้วย Morphology
    kernel = np.ones((3, 3), np.uint8)
    mask = cv2.dilate(mask, kernel, iterations=1)

    # ตัด noise รอบนอก (Crop เฉพาะบริเวณเส้นแบ่งกลาง)
    # 👉 ปรับพิกัด (y:y+h, x:x+w) ตามตำแหน่งเส้นแบ่งกลาง
    h, w = frame.shape[:2]
    cropped_mask = mask[int(h/3):int(h*2/3), int(w/3):int(w*2/3)]
    cropped_frame = frame[int(h/3):int(h*2/3), int(w/3):int(w*2/3)]

    # ตรวจจับเส้นแบ่งใน mask
    edges = cv2.Canny(cropped_mask, 50, 150, apertureSize=3)
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=30, minLineLength=30, maxLineGap=10)

    angle = None
    if lines is not None:
        # หาเส้นที่ยาวที่สุด
        longest = max(lines, key=lambda line: np.hypot(line[0][2]-line[0][0], line[0][3]-line[0][1]))
        x1, y1, x2, y2 = longest[0]

        # วาดเส้นแบ่งบน cropped_frame
        cv2.line(cropped_frame, (x1, y1), (x2, y2), (0, 0, 255), 2)

        # คำนวณมุม
        angle = math.degrees(math.atan2(y2 - y1, x2 - x1)) % 360

        # baseline_angle = มุมแรก
        if baseline_angle is None:
            baseline_angle = angle

        # มุม relative (0° baseline)
        relative_angle = (angle - baseline_angle + 360) % 360
        angles.append(relative_angle)

        # Overlay
        text = f"Rel.Angle: {relative_angle:.2f} deg"
        cv2.putText(cropped_frame, text, (10, 30),
                     cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    else:
        text = "No Line Detected"
        cv2.putText(cropped_frame, text, (10, 30),
                     cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

    # แปะ cropped_frame กลับเข้าไปใน frame
    frame[int(h/3):int(h*2/3), int(w/3):int(w*2/3)] = cropped_frame

    # บันทึกวิดีโอ
    out.write(frame)

    # แสดงผล
    cv2.imshow('Detect Blue Line', frame)
    if cv2.waitKey(delay) & 0xFF == ord('q'):
        break

cap.release()
out.release()
cv2.destroyAllWindows()

# สรุป: export มุมทั้งหมดเป็น CSV
import pandas as pd
df = pd.DataFrame({
    'frame_check': range(1, len(angles) + 1),
    'relative_angle': angles
})
df.to_csv('detected_blue_line_angles.csv', index=False)

print("✅ เสร็จแล้ว! บันทึกไฟล์: output_detect_blue_line.mp4 + detected_blue_line_angles.csv")
