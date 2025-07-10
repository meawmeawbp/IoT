import cv2
import random
import os

# เปิดวิดีโอ
cap = cv2.VideoCapture(r'C:\miewmiew\Hackathon\IoT\checkcheck\hsv_output2.mp4')
output_dir = 'random_crops'
os.makedirs(output_dir, exist_ok=True)

frame_count = 0
crop_count = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_count += 1

    # ทุก 30 frame (1 วินาทีโดยประมาณ) → สุ่ม crop
    if frame_count % 30 == 0:
        h, w, _ = frame.shape
        crop_w, crop_h = int(w * 0.3), int(h * 0.3)  # ขนาด crop 30%
        x = random.randint(0, w - crop_w)
        y = random.randint(0, h - crop_h)

        crop = frame[y:y+crop_h, x:x+crop_w]
        crop_count += 1
        filename = f'{output_dir}/crop_{crop_count:03d}.jpg'
        cv2.imwrite(filename, crop)

cap.release()
print(f"✅ สุ่ม crop ได้ {crop_count} รูป เก็บในโฟลเดอร์: {output_dir}")
