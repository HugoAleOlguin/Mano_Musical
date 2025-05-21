import cv2
from hand_detector import HandDetector
from audio_player import AudioPlayer
from visual_overlays import PianoKeyboard, StatusOverlay  # Actualizado
from visual_elements import PerformanceMetrics
from visual_effects import GeometricVisualizer
import time

def main():
    cap = cv2.VideoCapture(0)
    # Establecer resolución más alta
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    detector = HandDetector()
    player = AudioPlayer()
    visualizer = GeometricVisualizer()
    
    # Crear ventana con tamaño ajustable
    cv2.namedWindow('Detector Musical de Manos', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Detector Musical de Manos', 1280, 720)
    
    # Variables para control de gestos
    last_gesture = None
    last_gesture_time = 0
    gesture_cooldown = 0.05  # Reducir a 50ms para transiciones más suaves
    
    # Configuración para el teclado virtual
    show_keyboard = True
    keyboard_config = {
        'position': (0.8, 0.9),
        'size': (300, 100)
    }
    
    # Configuración visual
    VISUAL_CONFIG = {
        'keyboard_style': {
            'size': (400, 150),
            'position': 'bottom_right',
            'show_black_keys': True,
            'rounded_corners': True,
            'animation_speed': 0.2
        },
        'theme': 'dark',
        'transparency': 0.8
    }
    
    # Inicializar métricas y estado
    metrics = PerformanceMetrics()
    start_time = time.time()
    current_note = None
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        # Voltear imagen horizontalmente para una experiencia más natural
        frame = cv2.flip(frame, 1)
        
        # Control de tiempo para gestos
        current_time = time.time()
        if current_time - last_gesture_time >= gesture_cooldown:
            gesture = detector.detect_hand(frame)
            if gesture != last_gesture:
                player.play_sound(gesture)
                last_gesture = gesture
                last_gesture_time = current_time
                
                # Actualizar nota actual cuando cambia el gesto
                current_note = "Silencio" if gesture == "dedos_0" else \
                              "Do" if gesture == "dedos_1" else \
                              "Re" if gesture == "dedos_2" else \
                              "Mi" if gesture == "dedos_3" else \
                              "Fa" if gesture == "dedos_4" else \
                              "Sol" if gesture == "dedos_5" else None
        
        # Actualizar métricas y tiempo de sesión
        metrics.update()
        current_time = time.time()
        session_time = current_time - start_time
        
        # Dibujar elementos visuales
        if show_keyboard and current_note:
            PianoKeyboard.draw(frame, current_note, VISUAL_CONFIG)
        visualizer.draw(frame, current_note or "Silencio", 
                       player.current_frequency or 0)
        StatusOverlay.draw(frame, gesture is not None, metrics.fps)
        PerformanceMetrics.draw(frame, metrics.fps, session_time)
        
        # Antes de mostrar el frame
        if current_note:
            visualizer.draw(frame, current_note, player.current_frequency)
        
        cv2.imshow('Detector Musical de Manos', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    player.stop_sound()
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()