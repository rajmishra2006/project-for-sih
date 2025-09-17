import cv2, mediapipe as mp, numpy as np
from cheat_detector import rule_based_check

mp_pose = mp.solutions.pose

def calculate_angle(a, b, c):
    ax, ay = a; bx, by = b; cx, cy = c
    ab = (ax-bx, ay-by); cb = (cx-bx, cy-by)
    dot = ab[0]*cb[0] + ab[1]*cb[1]
    magab = np.hypot(ab[0], ab[1]); magcb = np.hypot(cb[0], cb[1])
    if magab*magcb == 0: return 0.0
    cosv = dot/(magab*magcb)
    cosv = max(-1.0, min(1.0, cosv))
    ang = np.degrees(np.arccos(cosv))
    if ang > 180.0:
        ang = 360.0 - ang
    return ang

def analyze_video(path):
    cap = cv2.VideoCapture(path)
    count, stage = 0, None
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        h,w,_ = frame.shape
        pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
        res = pose.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        if res.pose_landmarks:
            lm = res.pose_landmarks.landmark
            hip = (lm[24].x*w, lm[24].y*h)
            knee = (lm[26].x*w, lm[26].y*h)
            ankle = (lm[28].x*w, lm[28].y*h)
            angle = calculate_angle(hip,knee,ankle)
            if angle < 90:
                stage = "down"
            if angle > 150 and stage == "down":
                count += 1
                stage = "up"
        pose.__del__()  # release per-frame pose to save resources
    cap.release()

    # cheat check
    cheat_result = {}
    try:
        cheat_result = rule_based_check(path)
    except Exception:
        cheat_result = {"decision":"UNKNOWN", "flags":[]}

    return {"count": count, "decision": cheat_result.get("decision","UNKNOWN"), "flags": cheat_result.get("flags",[])}
