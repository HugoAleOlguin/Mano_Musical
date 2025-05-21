import time
import cv2
import numpy as np

class PerformanceMetrics:
    def __init__(self):
        self.start_time = time.time()
        self.frame_count = 0
        self.fps = 0
        
    def update(self):
        self.frame_count += 1
        elapsed_time = time.time() - self.start_time
        self.fps = self.frame_count / elapsed_time
        
    @staticmethod
    def draw(frame, fps, session_time):
        height, width = frame.shape[:2]
        # Tiempo de sesión en la esquina superior derecha
        minutes = int(session_time // 60)
        seconds = int(session_time % 60)
        cv2.putText(frame, f"Tiempo: {minutes:02d}:{seconds:02d}",
                   (width - 200, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
