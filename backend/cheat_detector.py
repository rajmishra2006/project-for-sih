import statistics, numpy as np
import cv2, mediapipe as mp

mp_pose = mp.solutions.pose

def rule_based_check(video_path):
    cap = cv2.VideoCapture(video_path)
    motion, vis = [], []
    prev_gray = None
    pose = mp_pose.Pose()
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret: break
        h,w,_ = frame.shape
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        res = pose.process(rgb)
        if res.pose_landmarks:
            vis.append(np.mean([l.visibility for l in res.pose_landmarks.landmark]))
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if prev_gray is not None:
            flow = cv2.calcOpticalFlowFarneback(prev_gray, gray, None,0.5,3,15,3,5,1.2,0)
            mag,_ = cv2.cartToPolar(flow[...,0], flow[...,1])
            motion.append(np.mean(mag))
        prev_gray = gray
    cap.release()
    flags, decision = [], "VALID"
    if vis and statistics.mean(vis) < 0.35:
        flags.append("low_pose_visibility")
    if motion and np.mean(motion) < 0.3:
        flags.append("low_motion")
    if "low_pose_visibility" in flags or "low_motion" in flags:
        decision = "CHEAT"
    return {"decision": decision, "flags": flags}
