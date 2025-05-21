import mediapipe as mp # type: ignore
import cv2
import numpy as np

class HandDetector:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.6,    # Reducir para mejor rendimiento
            min_tracking_confidence=0.5,     # Reducir para mejor rendimiento
            model_complexity=0               # Usar modelo más ligero
        )
        self.mp_draw = mp.solutions.drawing_utils
        self.previous_gesture = None

    def detect_hand(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)
        
        if results.multi_hand_landmarks:
            landmarks = results.multi_hand_landmarks[0]
            self.mp_draw.draw_landmarks(frame, landmarks, self.mp_hands.HAND_CONNECTIONS)
            return self._get_hand_gesture(landmarks, frame)
        return None

    def _get_hand_gesture(self, landmarks, frame):
        fingers = [0] * 5
        
        # Pulgar: comparar posición horizontal
        thumb_tip = landmarks.landmark[4]
        thumb_base = landmarks.landmark[2]
        
        # Si el pulgar está más a la izquierda que su base
        if thumb_tip.x < thumb_base.x - 0.05:
            fingers[0] = 1
        
        # Para los otros dedos: comparar altura
        tips = [8, 12, 16, 20]  # puntas de los dedos
        mcp = [5, 9, 13, 17]    # articulaciones base
        
        for i in range(4):
            if landmarks.landmark[tips[i]].y < landmarks.landmark[mcp[i]].y - 0.1:
                fingers[i + 1] = 1
        
        total_fingers = sum(fingers)
        return f"dedos_{total_fingers}"