from ultralytics import YOLO
import cv2, numpy as np, pyttsx3
import time

def get_angle(a, b, c):
    ba, bc = a - b, c - b
    cosine = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc) + 1e-6)
    return np.degrees(np.arccos(np.clip(cosine, -1.0, 1.0)))

engine = pyttsx3.init()
model = YOLO('yolov8m-pose.pt')
face_model = YOLO('yolov8n-face.pt')  # Make sure this file is present

cap = cv2.VideoCapture(0)
writer = None

rep_state = 'down'
rep_count, good_reps, bad_reps = 0, 0, 0
bad_reason = ''

# Thresholds (tune as needed)
RAISE_HEIGHT_THRESH = 0.05  # fraction of frame height above shoulder
ELBOW_STRAIGHT_THRESH = 160 # degrees

while True:
    ret, frame = cap.read()
    if not ret: break
    frame = cv2.flip(frame, 1)  # Mirror for webcam

    # --- Face blurring ---
    face_results = face_model(frame, imgsz=320, conf=0.5)
    for face in face_results[0].boxes.xyxy.cpu().numpy() if face_results[0].boxes is not None else []:
        x1, y1, x2, y2 = map(int, face)
        x1, y1 = max(0, x1), max(0, y1)
        x2, y2 = min(frame.shape[1], x2), min(frame.shape[0], y2)
        face_roi = frame[y1:y2, x1:x2]
        if face_roi.size > 0:
            face_roi = cv2.GaussianBlur(face_roi, (31, 31), 30)
            frame[y1:y2, x1:x2] = face_roi

    results = model(frame, imgsz=640)
    kps = results[0].keypoints.xy[0].cpu().numpy() if results[0].keypoints else None
    if kps is None or kps.shape[0] < 17:
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
        if elbows_straight:
            good_reps += 1
            feedback = f"{rep_count} - Well done"
            bad_reason = ''
        else:
            bad_reps += 1
            reasons = []
            if not elbows_straight: reasons.append("elbow bent")
            bad_reason = ', '.join(reasons)
            feedback = f"{rep_count} - Bad rep ({bad_reason})"
        engine.say(feedback)
        engine.runAndWait()

    # Alerts for not raising hands high enough
    if rep_state == 'down' and not hands_high:
        cv2.putText(frame, "Raise your hands higher!", (30, 330), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 165, 255), 2)
        engine.say("Raise your hands higher!")
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

    cv2.imshow('Lateral Raise Feedback', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'): break

cap.release()
cv2.destroyAllWindows() 