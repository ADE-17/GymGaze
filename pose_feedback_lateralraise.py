import cv2, numpy as np, pyttsx3, random
from ultralytics import YOLO
import time

def get_angle(a, b, c):
    ba, bc = a - b, c - b
    cosine = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc) + 1e-6)
    return np.degrees(np.arccos(np.clip(cosine, -1.0, 1.0)))

def draw_gamified_overlay(frame, rep_count, good_reps, bad_reps, feedback, bad_reason, color, avg_score, total=10):
    h, w = frame.shape[:2]
    # Top bar (reps)
    cv2.rectangle(frame, (20, 20), (w-20, 80), (30,30,30), -1)
    bar_w = int((w-60) * min(rep_count/total, 1.0))
    cv2.rectangle(frame, (30, 30), (30+bar_w, 70), color, -1)
    cv2.putText(frame, f"Reps: {rep_count}", (40, 65), cv2.FONT_HERSHEY_DUPLEX, 1, (255,255,255), 2)
    # Left vertical bar (good reps)
    cv2.rectangle(frame, (10, 100), (70, h-100), (0,80,0), -1)
    good_bar_h = int((h-200) * min(good_reps/max(1, rep_count), 1.0)) if rep_count else 0
    cv2.rectangle(frame, (20, h-100-good_bar_h), (60, h-100), (0,255,0), -1)
    cv2.putText(frame, f"{good_reps}", (25, h-110), cv2.FONT_HERSHEY_DUPLEX, 1, (255,255,255), 2)
    cv2.putText(frame, "+", (35, h-130), cv2.FONT_HERSHEY_DUPLEX, 1.5, (0,255,0), 3)
    # Right vertical bar (bad reps)
    cv2.rectangle(frame, (w-70, 100), (w-10, h-100), (40,0,0), -1)
    bad_bar_h = int((h-200) * min(bad_reps/max(1, rep_count), 1.0)) if rep_count else 0
    cv2.rectangle(frame, (w-60, h-100-bad_bar_h), (w-20, h-100), (0,0,255), -1)
    cv2.putText(frame, f"{bad_reps}", (w-55, h-110), cv2.FONT_HERSHEY_DUPLEX, 1, (255,255,255), 2)
    cv2.putText(frame, "-", (w-45, h-130), cv2.FONT_HERSHEY_DUPLEX, 1.5, (0,0,255), 3)
    # Feedback
    if feedback:
        cv2.putText(frame, feedback, (40, 120), cv2.FONT_HERSHEY_COMPLEX, 1.1, color, 2)
    if bad_reason:
        cv2.putText(frame, f"Reason: {bad_reason}", (40, 170), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,0,255), 2)
    # Running total score at bottom center
    if avg_score is not None:
        score_color = (0,255,0) if avg_score>=80 else (0,165,255) if avg_score>=60 else (0,0,255)
        cv2.rectangle(frame, (w//2-120, h-80), (w//2+120, h-30), (40,40,80), -1)
        cv2.rectangle(frame, (w//2-120, h-80), (w//2+120, h-30), (255,215,0), 3)
        cv2.putText(frame, f"Score: {avg_score}/100", (w//2-100, h-40), cv2.FONT_HERSHEY_DUPLEX, 1.5, score_color, 4)
    return frame

def blur_face_eyes(frame, kps):
    if kps.shape[0] > 5:
        left_eye = kps[2]
        right_eye = kps[5]
        center = ((left_eye + right_eye) / 2).astype(int)
        eye_dist = np.linalg.norm(left_eye - right_eye)
        r = int(eye_dist * 1.2)
        x, y = int(center[0]), int(center[1])
        x1, y1 = max(0, x-r), max(0, y-r)
        x2, y2 = min(frame.shape[1], x+r), min(frame.shape[0], y+r)
        roi = frame[y1:y2, x1:x2]
        if roi.size > 0:
            mask = np.zeros((y2-y1, x2-x1), dtype=np.uint8)
            cx = min(r, x2-x1-1)
            cy = min(r, y2-y1-1)
            cv2.circle(mask, (cx, cy), r, 255, -1)
            blurred = cv2.GaussianBlur(roi, (51, 51), 50)
            roi[mask==255] = blurred[mask==255]
            frame[y1:y2, x1:x2] = roi
    return frame

# Use a different voice if available
engine = pyttsx3.init()
voices = engine.getProperty('voices')
if len(voices) > 1:
    engine.setProperty('voice', voices[1].id)
model = YOLO('yolov8m-pose.pt')

cap = cv2.VideoCapture(0)
writer = None

rep_state = 'down'
rep_count, good_reps, bad_reps = 0, 0, 0
bad_reason = ''
feedback = ''
rep_scores = []
cheer_reps = [3, 4, 7, 10, 15, 20]
last_cheer = 0

# Thresholds (tune as needed)
RAISE_HEIGHT_THRESH = 0.05  # fraction of frame height above shoulder
ELBOW_STRAIGHT_THRESH = 160 # degrees

while True:
    ret, frame = cap.read()
    if not ret: break
    frame = cv2.flip(frame, 1)
    results = model(frame, imgsz=416)
    kps_all = [k.xy[0].cpu().numpy() for k in results[0].keypoints] if results[0].keypoints is not None else []
    for kps in kps_all:
        if kps.shape[0] > 5:
            frame = blur_face_eyes(frame, kps)
    kps = results[0].keypoints.xy[0].cpu().numpy() if results[0].keypoints else None
    if kps is None or kps.shape[0] < 11:
        cv2.imshow('Lateral Raise Feedback', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'): break
        continue

    # Keypoints
    l_shoulder, r_shoulder = kps[5], kps[6]
    l_elbow, r_elbow = kps[7], kps[8]
    l_wrist, r_wrist = kps[9], kps[10]

    # Use average for both arms
    shoulder_y = (l_shoulder[1] + r_shoulder[1]) / 2
    frame_height = frame.shape[0]
    raise_thresh = shoulder_y - RAISE_HEIGHT_THRESH * frame_height
    hands_high = (l_wrist[1] < raise_thresh) and (r_wrist[1] < raise_thresh)

    # Elbow angles (both arms)
    l_elbow_angle = get_angle(l_shoulder, l_elbow, l_wrist)
    r_elbow_angle = get_angle(r_shoulder, r_elbow, r_wrist)
    elbows_straight = (l_elbow_angle > ELBOW_STRAIGHT_THRESH) and (r_elbow_angle > ELBOW_STRAIGHT_THRESH)

    # Status display
    if hands_high:
        status = "Status: Up"
    else:
        status = "Status: Down"

    # Rep tracking logic
    if rep_state == 'down' and hands_high:
        rep_state = 'up'
        bad_reason = ''
        if not elbows_straight:
            cv2.putText(frame, "Warning: Straighten your arms!", (30, 300), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 165, 255), 2)
            engine.say("Straighten your arms!")
            engine.runAndWait()
    elif rep_state == 'up' and not hands_high:
        rep_state = 'down'
        rep_count += 1
        # --- Scoring ---
        score = 100
        if not elbows_straight:
            score -= 40
        score = max(0, score)
        rep_scores.append(score)
        if elbows_straight:
            good_reps += 1
            feedback = f"{rep_count} - Well done"
            bad_reason = ''
            # Cheer after 3, 4, 7, 10, 15, 20 reps
            if rep_count in cheer_reps and rep_count != last_cheer:
                engine.say(random.choice(["Come on, keep it up!", "Great job!", "You're on fire!", "Awesome, keep going!"]))
                engine.runAndWait()
                last_cheer = rep_count
        else:
            bad_reps += 1
            reasons = []
            if not elbows_straight: reasons.append("elbow bent")
            bad_reason = ', '.join(reasons)
            feedback = f"{rep_count} - Bad rep ({bad_reason})"
        engine.say(feedback)
        engine.runAndWait()

    # Skeleton drawing
    pairs = [(5,7),(7,9),(6,8),(8,10),(5,6)]
    for i,j in pairs:
        if all(kps[[i,j],0] > 0): cv2.line(frame, tuple(kps[i].astype(int)), tuple(kps[j].astype(int)), (0,255,255), 2)
    for pt in kps[[5,6,7,8,9,10]]: cv2.circle(frame, tuple(pt.astype(int)), 4, (0,255,0), -1)

    # Overlay text
    cv2.putText(frame, status, (30,60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
    cv2.putText(frame, f"Total Reps: {rep_count}", (30,100), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2)
    cv2.putText(frame, f"Good Reps: {good_reps}", (30,130), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)
    cv2.putText(frame, f"Bad Reps: {bad_reps}", (30,160), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255), 2)
    if bad_reason: cv2.putText(frame, f"Reason: {bad_reason}", (30,190), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)
    cv2.putText(frame, f"L Elbow: {l_elbow_angle:.1f} deg", (30, 220), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,0), 2)
    cv2.putText(frame, f"R Elbow: {r_elbow_angle:.1f} deg", (30, 245), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,0), 2)

    avg_score = int(sum(rep_scores) / len(rep_scores)) if rep_scores else None
    frame = draw_gamified_overlay(frame, rep_count, good_reps, bad_reps, feedback, bad_reason, (0,255,0) if elbows_straight else (0,0,255), avg_score)

    cv2.imshow('Lateral Raise Feedback', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'): break

cap.release()
cv2.destroyAllWindows() 