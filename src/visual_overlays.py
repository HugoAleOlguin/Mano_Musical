import cv2
import numpy as np
from time import time

class PianoKeyboard:
    WHITE_NOTES = ['Do', 'Re', 'Mi', 'Fa', 'Sol']
    BLACK_NOTES = ['Do#', 'Re#', '', 'Fa#', 'Sol#']
    
    @staticmethod
    def draw(frame, current_note, config):
        height, width = frame.shape[:2]
        keyboard_width = config['keyboard_style']['size'][0]
        keyboard_height = config['keyboard_style']['size'][1]
        
        # Posición del teclado
        if config['keyboard_style']['position'] == 'bottom_right':
            start_x = width - keyboard_width - 20
            start_y = height - keyboard_height - 20
        
        # Dibujar teclas blancas
        white_key_width = keyboard_width // len(PianoKeyboard.WHITE_NOTES)
        for i, note in enumerate(PianoKeyboard.WHITE_NOTES):
            x = start_x + i * white_key_width
            
            # Efecto 3D y sombras
            if note == current_note:
                color = (200, 200, 255)
                shadow_offset = 5
            else:
                color = (255, 255, 255)
                shadow_offset = 2
                
            # Tecla con bordes redondeados
            cv2.rectangle(frame, 
                        (x + shadow_offset, start_y + shadow_offset),
                        (x + white_key_width, start_y + keyboard_height),
                        (100, 100, 100), -1)  # Sombra
            
            pts = np.array([
                [x, start_y],
                [x + white_key_width, start_y],
                [x + white_key_width, start_y + keyboard_height],
                [x, start_y + keyboard_height]
            ], np.int32)
            
            cv2.fillPoly(frame, [pts], color)
            cv2.polylines(frame, [pts], True, (0, 0, 0), 2)
            
            # Texto de nota
            cv2.putText(frame, note, 
                       (x + 5, start_y + keyboard_height - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)

        # Dibujar teclas negras si está habilitado
        if config['keyboard_style']['show_black_keys']:
            black_key_width = white_key_width // 2
            for i, note in enumerate(PianoKeyboard.BLACK_NOTES):
                if note:  # Solo dibujar si hay nota negra
                    x = start_x + (i * white_key_width) + (white_key_width // 2)
                    cv2.rectangle(frame,
                                (x, start_y),
                                (x + black_key_width, start_y + (keyboard_height * 2//3)),
                                (40, 40, 40), -1)

class StatusOverlay:
    @staticmethod
    def draw(frame, hand_detected, fps):  # Eliminado last_notes del parámetro
        height, width = frame.shape[:2]
        
        # FPS encima del indicador
        cv2.putText(frame, f"FPS: {int(fps)}", (10, 20),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        # Indicador de detección de mano
        color = (0, 255, 0) if hand_detected else (0, 0, 255)
        cv2.circle(frame, (30, 40), 10, color, -1)
