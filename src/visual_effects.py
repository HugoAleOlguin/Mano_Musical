import cv2
import numpy as np
from math import sin, cos, pi

class GeometricVisualizer:
    def __init__(self):
        self.time = 0
        self.particles = []
        self.visualizer_size = (200, 200)  # Reducido a 200x200
        self.border_color = (0, 0, 0)
        self.border_thickness = 2
        self.color_schemes = {
            'Do': [(255,50,50), (255,0,0)],      # Rojo más intenso
            'Re': [(50,255,50), (0,255,0)],      # Verde más vivo
            'Mi': [(50,50,255), (0,0,255)],      # Azul brillante
            'Fa': [(255,50,255), (255,0,255)],   # Magenta intenso
            'Sol': [(255,255,50), (255,255,0)],  # Amarillo brillante
            'Silencio': [(30,30,30), (0,0,0)]    # Tonos oscuros
        }
        self.effect_intensity = 0
        self.rotation = 0

    def draw(self, frame, current_note, frequency):
        viz_canvas = np.zeros((*self.visualizer_size, 3), dtype=np.uint8)
        
        if current_note != "Silencio":
            self.time += 0.05
            self._draw_effects(viz_canvas, frequency, current_note)
        else:
            # Estado silencio con efecto sutil
            self.effect_intensity *= 0.95
            self._draw_effects(viz_canvas, 0, 'Silencio')
        
        # Borde con glow
        glow_color = self.color_schemes[current_note][0] if current_note != "Silencio" else (30,30,30)
        cv2.rectangle(viz_canvas, (0, 0), 
                     (self.visualizer_size[0]-1, self.visualizer_size[1]-1),
                     glow_color, 3)
        cv2.rectangle(viz_canvas, (2, 2),
                     (self.visualizer_size[0]-3, self.visualizer_size[1]-3),
                     self.border_color, self.border_thickness)

        # Posicionar en esquina inferior izquierda
        height, width = frame.shape[:2]
        roi_y = height - self.visualizer_size[1] - 20
        roi_x = 20
        
        # Mezclar con más contraste
        roi = frame[roi_y:roi_y + self.visualizer_size[1], 
                   roi_x:roi_x + self.visualizer_size[0]]
        cv2.addWeighted(roi, 0.2, viz_canvas, 0.8, 0, roi)

    def _draw_effects(self, canvas, frequency, note):
        colors = self.color_schemes.get(note, [(255,255,255)])
        center = (self.visualizer_size[0]//2, self.visualizer_size[1]//2)
        
        # Efecto de ondas pulsantes
        self.effect_intensity = min(1.0, self.effect_intensity + 0.1)
        wave_size = int(30 * self.effect_intensity)
        self.rotation += 0.1

        # Fondo dinámico
        for r in range(0, 100, 10):
            alpha = max(0.1, 0.7 - (r/100))
            radius = max(1, int(r + sin(self.time * 3) * wave_size))
            cv2.circle(canvas, center, radius, 
                      tuple(int(c*alpha) for c in colors[0]), 1)

        # Estrellas giratorias
        for i in range(5):
            angle = self.rotation + (i * 2 * pi / 5)
            radius = max(1, int(40 + sin(self.time * 2) * 10))
            x = int(center[0] + cos(angle) * radius)
            y = int(center[1] + sin(angle) * radius)
            cv2.line(canvas, center, (x, y), colors[0], 2)

        # Círculos concéntricos pulsantes
        for i in range(3):
            radius = max(1, int(20 + i*15 + sin(self.time*3 + i)*10))
            cv2.circle(canvas, center, radius, colors[1], 1)

        # Efecto de partículas en espiral
        for i in range(12):
            angle = self.time + (i * pi / 6)
            r = max(1, int(20 + sin(self.time * 2) * 10))
            x = int(center[0] + cos(angle) * r)
            y = int(center[1] + sin(angle) * r)
            size = max(1, int(3 + sin(self.time + i) * 2))
            cv2.circle(canvas, (x, y), size, colors[0], -1)

    def _update_particles(self, note):
        # Añadir nuevas partículas
        if note and len(self.particles) < 100:
            colors = self.color_schemes.get(note, [(255,255,255)])
            self.particles.append({
                'pos': [np.random.randint(0, self.visualizer_size[0]), np.random.randint(0, self.visualizer_size[1])],
                'vel': [np.random.randn()*2, np.random.randn()*2],
                'life': 1.0,
                'color': colors[0]
            })
        
        # Actualizar partículas existentes
        self.particles = [p for p in self.particles if p['life'] > 0]
        for p in self.particles:
            p['pos'][0] += p['vel'][0]
            p['pos'][1] += p['vel'][1]
            p['life'] -= 0.01

    def _draw_particles(self, canvas):
        for p in self.particles:
            pos = tuple(map(int, p['pos']))
            color = tuple(int(c * p['life']) for c in p['color'])
            size = int(10 * p['life'])
            cv2.circle(canvas, pos, size, color, -1)
