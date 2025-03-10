import cv2
import mediapipe as mp
import numpy as np
import pyttsx3
import matplotlib.pyplot as plt
import threading

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
def speak(text):
    threading.Thread(target=lambda: (engine.say(text), engine.runAndWait())).start()

engine = pyttsx3.init()

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

cap = cv2.VideoCapture(0)
cap.set(3, 320)  # Reduce frame width
cap.set(4, 240)  # Reduce frame height

squat_counter = 0
set_counter = 0
stage = None  # 'down' or 'up'
total_reps_per_set = 10
calories_burned = 0.0

speak_flag = {"lower_hips": False, "lock_knees": False, "squat_down": False, "squat_up": False}

time_series = []
angle_series = []
frame_count = 0

plt.ion()
fig, ax = plt.subplots()
ax.set_ylim(0, 180)
ax.set_xlabel("Time")
ax.set_ylabel("Knee Angle")
line, = ax.plot(time_series, angle_series, 'r-')

with mp_pose.Pose(min_detection_confidence=0.7, min_tracking_confidence=0.7) as pose:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        frame = cv2.resize(frame, (640, 480))  # Resize for performance
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
                if not speak_flag["squat_down"]:
                    speak("Squat down")
                    speak_flag["squat_down"] = True
                    speak_flag["squat_up"] = False
            if angle > 160 and stage == "down":  # Up position
                stage = "up"
                squat_counter += 1
                calories_burned += 0.32  # Approximate calories per squat
                if not speak_flag["squat_up"]:
                    speak(f"Squat count {squat_counter}")
                    speak_flag["squat_up"] = True
                    speak_flag["squat_down"] = False
                if squat_counter % total_reps_per_set == 0:
                    set_counter += 1
                    speak(f"Set {set_counter} completed")
            
            # Store data for real-time graph every 5 frames
            frame_count += 1
            if frame_count % 5 == 0:
                time_series.append(frame_count)
                angle_series.append(angle)
                if len(time_series) > 50:
                    time_series.pop(0)
                    angle_series.pop(0)
                
                # Update graph
                line.set_xdata(time_series)
                line.set_ydata(angle_series)
                ax.relim()
                ax.autoscale_view()
                plt.draw()
                plt.pause(0.001)
            
            # Display stats
            cv2.putText(frame, f'Squats: {squat_counter}', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            cv2.putText(frame, f'Sets: {set_counter}', (50, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)
            cv2.putText(frame, f'Calories: {calories_burned:.2f}', (50, 130), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
            cv2.putText(frame, f'Angle: {int(angle)}', (50, 170), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            # Form correction feedback
            if angle < 60 and not speak_flag["lower_hips"]:
                cv2.putText(frame, "Lower your hips!", (50, 210), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                speak("Lower your hips")
                speak_flag["lower_hips"] = True
            elif angle >= 60:
                speak_flag["lower_hips"] = False
            
            if angle > 170 and not speak_flag["lock_knees"]:
                cv2.putText(frame, "Don't lock knees!", (50, 250), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                speak("Don't lock your knees")
                speak_flag["lock_knees"] = True
            elif angle <= 160:
                speak_flag["lock_knees"] = False
        
        cv2.imshow('Squat Tracker', frame)
        
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
plt.close()
