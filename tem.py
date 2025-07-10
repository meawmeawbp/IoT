import cv2
import numpy as np

# โหลดวิดีโอ
video_path = r'C:\miewmiew\Hackathon\IoT\checkcheck\hsv_output2.mp4'
cap = cv2.VideoCapture(video_path)

# โหลด template หลายรูป (grayscale)
templates = [
    cv2.imread('tem1.png', 0),
    cv2.imread('tem2.png', 0),
    cv2.imread('tem3.png', 0),
    cv2.imread('tem4.png', 0),
    cv2.imread('tem5.png', 0)
]
template_names = ['template1', 'template2', 'template3', 'template4', 'template5']
template_sizes = [(t.shape[::-1]) for t in templates]  # (w, h) ของแต่ละ template

# ตั้งค่าการบันทึกวิดีโอ
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('output_template_matching.mp4', fourcc, cap.get(cv2.CAP_PROP_FPS),
                      (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))

# ตรวจจับทุก 3 วินาที (ตาม FPS จริง)
fps = cap.get(cv2.CAP_PROP_FPS)
frames_per_3sec = int(fps * 3)
frame_count = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame_count += 1

    # ตรวจจับทุก 3 วินาที
    if frame_count % frames_per_3sec != 0:
        out.write(frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        continue

    # แปลงเป็น grayscale
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # วนลูปทีละ template
    for idx, template in enumerate(templates):
        w, h = template_sizes[idx]

        # Template Matching
        res = cv2.matchTemplate(frame_gray, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        # แสดงตำแหน่งที่เจอ template
        top_left = max_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)
        cv2.rectangle(frame, top_left, bottom_right, (0, 255, 0), 2)

        # Overlay
        text = f"{template_names[idx]}: {max_val:.2f}"
        cv2.putText(frame, text, (top_left[0], top_left[1] - 10),
                     cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    # บันทึกวิดีโอ
    out.write(frame)

    # แสดงผล
    cv2.imshow('Template Match', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
out.release()
cv2.destroyAllWindows()
print("✅ เสร็จแล้ว! บันทึกไฟล์: output_template_matching.mp4")
