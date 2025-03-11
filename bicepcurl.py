import cv2
import mediapipe as mp
import numpy as np

# Initialize Mediapipe Pose
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# Video capture
cap = cv2.VideoCapture(0)

# Bicep curl variables
left_reps = 0
right_reps = 0
left_curling = False  # Track left arm movement
right_curling = False  # Track right arm movement

# Open Mediapipe Pose
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)  # Flip for mirror effect
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(rgb_frame)

        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark

            # Left arm landmarks
            left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
            left_elbow = landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value]
            left_wrist = landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value]

            # Right arm landmarks
            right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
            right_elbow = landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value]
            right_wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value]

            def calculate_angle(a, b, c):
                """Calculate angle between three points (shoulder, elbow, wrist)."""
                a = np.array([a.x, a.y])
                b = np.array([b.x, b.y])
                c = np.array([c.x, c.y])

                ba = a - b
                bc = c - b

                cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
                angle = np.arccos(np.clip(cosine_angle, -1.0, 1.0))
                return np.degrees(angle)

            # Calculate elbow angles
            left_angle = calculate_angle(left_shoulder, left_elbow, left_wrist)
            right_angle = calculate_angle(right_shoulder, right_elbow, right_wrist)

            # Left arm bicep curl detection
            if left_angle < 50 and not left_curling:  # Curl completed
                left_curling = True
            elif left_angle > 140 and left_curling:  # Arm fully extended
                left_reps += 1
                left_curling = False  # Reset for next curl

            # Right arm bicep curl detection
            if right_angle < 50 and not right_curling:  # Curl completed
                right_curling = True
            elif right_angle > 140 and right_curling:  # Arm fully extended
                right_reps += 1
                right_curling = False  # Reset for next curl

            # Display rep count
            cv2.putText(frame, f'Left Reps: {left_reps}', (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            cv2.putText(frame, f'Right Reps: {right_reps}', (50, 100),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

            # Draw pose landmarks
            mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        cv2.imshow("Bicep Curl Counter", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

cap.release()
cv2.destroyAllWindows()
