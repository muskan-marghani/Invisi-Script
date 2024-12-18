import streamlit as st
import cv2
import os
os.environ['TF_ENABLE_ONEDNN_OPTS']='0'
os.environ['KMP_DUPLICATE_LIB_OK']='True'
import mediapipe as mp
import numpy as np
from TextConverter import con
  
def air_canvas():
    # Initialize MediaPipe
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.8, min_tracking_confidence=0.8)
    mp_drawing = mp.solutions.drawing_utils

    # Streamlit app title and instructions
    st.text("Gesture Instructions:\n"
            "- Index finger up: Draw\n"
            "- Index and middle fingers up: Move\n"
            "- Thumbs up: Clear the canvas\n"
            "- Pinky finger up: Capture and save the canvas snapshot")

    # Create a placeholder for video feed
    canvas_placeholder = st.empty()

    # Set up canvas variables
    canvas = np.ones((480, 640, 3), dtype="uint8") * 255
    x_prev, y_prev = 0, 0

    # Start video capture
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        st.error("Could not open the camera.")
    else:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                st.error("Failed to capture image from camera.")
                break
            
            # Flip the frame for natural interaction
            frame = cv2.flip(frame, 1)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(frame_rgb)

            # Draw landmarks and handle gestures if hand is detected
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                    
                    # Extract coordinates of key landmarks
                    landmarks = hand_landmarks.landmark
                    x_index_finger = int(landmarks[8].x * frame.shape[1])
                    y_index_finger = int(landmarks[8].y * frame.shape[0])
                    x_thumb = int(landmarks[4].x * frame.shape[1])
                    y_thumb = int(landmarks[4].y * frame.shape[0])
                    x_middle_finger = int(landmarks[12].x * frame.shape[1])
                    y_middle_finger = int(landmarks[12].y * frame.shape[0])
                    x_pinky = int(landmarks[20].x * frame.shape[1])
                    y_pinky = int(landmarks[20].y * frame.shape[0])

                    # Distance calculations to determine gesture actions
                    distance_index_thumb = np.hypot(x_index_finger - x_thumb, y_index_finger - y_thumb)
                    distance_index_middle = np.hypot(x_middle_finger - x_index_finger, y_middle_finger - y_index_finger)
                    distance_index_pinky = np.hypot(x_pinky - x_index_finger, y_pinky - y_index_finger)

                    # Gesture: Draw when only the index finger is up
                    if distance_index_thumb > 40 and distance_index_middle > 50 and distance_index_pinky > 50:
                        if x_prev == 0 and y_prev == 0:
                            x_prev, y_prev = x_index_finger, y_index_finger
                        cv2.line(canvas, (x_prev, y_prev), (x_index_finger, y_index_finger), (0, 0, 0), 5)
                        x_prev, y_prev = x_index_finger, y_index_finger

                    # Gesture: Clear the canvas (thumbs up)
                    elif distance_index_thumb < 60 and distance_index_middle > 50 and distance_index_pinky > 50:
                        canvas = np.ones((frame.shape[0], frame.shape[1], 3), dtype=np.uint8) * 255
                        x_prev, y_prev = 0, 0  # Reset previous position to avoid connecting lines

                    # Gesture: Capture canvas (pinky finger up)
                    elif distance_index_pinky < 50:
                        cv2.imwrite("captured_canvas.png", canvas)
                        extracted_text = con('captured_canvas.png')
                        print(extracted_text)

                    else:
                        x_prev, y_prev = 0, 0  # Reset previous position

            # Adjust blending ratio to make the canvas overlay more natural
            alpha = 0.2  # Transparency level (0 = only frame, 1 = only canvas)
            combined_image = cv2.addWeighted(canvas, alpha, frame, 1 - alpha, 0)

            # Display the image in Streamlit
            canvas_placeholder.image(combined_image, channels="BGR")

        # Release resources
        cap.release()
        cv2.destroyAllWindows()
