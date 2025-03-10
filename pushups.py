import cv2
import mediapipe as mp
import numpy as np
import pyttsx3

def calculate_angle(a, b, c):
    """Calculate the angle between three points."""
    a = np.array(a)  # Hip
    b = np.array(b)  # Knee
    c = np.array(c)  # Ankle
    
    ba = a - b
    bc = c - b
    
    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    angle = np.arccos(np.clip(cosine_angle, -1.0, 1.0))  # Ensure within valid range
    return np.degrees(angle)

# Initialize text-to-speech engine
engine = pyttsx3.init()
def speak(text):
    engine.say(text)
    engine.runAndWait()

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

cap = cv2.VideoCapture(0)

squat_counter = 0
stage = None  # 'down' or 'up'

with mp_pose.Pose(min_detection_confidence=0.7, min_tracking_confidence=0.7) as pose:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = pose.process(frame)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        
        if result.pose_landmarks:
            landmarks = result.pose_landmarks.landmark
            
            # Extract key points
            hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP].x, landmarks[mp_pose.PoseLandmark.RIGHT_HIP].y]
            knee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE].x, landmarks[mp_pose.PoseLandmark.RIGHT_KNEE].y]
            ankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE].x, landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE].y]
            
            # Calculate knee angle
            angle = calculate_angle(hip, knee, ankle)
            
            # Squat logic
            if angle < 90 and stage != "down":  # Down position
                stage = "down"
                speak("Squat down")
            if angle > 160 and stage == "down":  # Up position
                stage = "up"
                squat_counter += 1
                speak(f"Squat count {squat_counter}")
            
            # Display squat count and angle
            cv2.putText(frame, f'Squats: {squat_counter}', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            cv2.putText(frame, f'Angle: {int(angle)}', (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            # Form correction feedback
            if angle < 60:
                cv2.putText(frame, "Lower your hips!", (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                speak("Lower your hips")
            if angle > 170:
                cv2.putText(frame, "Don't lock knees!", (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                speak("Don't lock your knees")
        
        cv2.imshow('Squat Tracker', frame)
        
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
