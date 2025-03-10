import torch
import cv2
import numpy as np
import mediapipe as mp
from time import time

def load_model(model_name='yolov5s'):
    model = torch.hub.load('ultralytics/yolov5', model_name, pretrained=True)
    return model

def detect_food_posture_hands(model):
    cap = cv2.VideoCapture(0)
    prev_time = 0
    
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose()
    
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands()
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break
        
        # Convert frame to RGB
        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = model(img_rgb)
        pose_results = pose.process(img_rgb)
        hand_results = hands.process(img_rgb)
        
        # Process food detection results
        for *box, conf, cls in results.xyxy[0]:
            x1, y1, x2, y2 = map(int, box)
            label = f"{model.names[int(cls)]} {conf:.2f}"
            
            # Draw bounding box
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        # Process posture tracking results
        if pose_results.pose_landmarks:
            for landmark in pose_results.pose_landmarks.landmark:
                h, w, _ = frame.shape
                cx, cy = int(landmark.x * w), int(landmark.y * h)
                cv2.circle(frame, (cx, cy), 5, (255, 0, 0), -1)
        
        # Process hand tracking results
        if hand_results.multi_hand_landmarks:
            for hand_landmarks in hand_results.multi_hand_landmarks:
                for landmark in hand_landmarks.landmark:
                    h, w, _ = frame.shape
                    cx, cy = int(landmark.x * w), int(landmark.y * h)
                    cv2.circle(frame, (cx, cy), 5, (0, 255, 255), -1)
        
        # Show FPS
        current_time = time()
        fps = 1 / (current_time - prev_time) if prev_time else 0
        prev_time = current_time
        cv2.putText(frame, f'FPS: {fps:.2f}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
        
        cv2.imshow("Food, Posture & Hand Detection", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    model = load_model('yolov5s')
    detect_food_posture_hands(model)
