# Mano Musical

Un instrumento musical virtual que permite tocar notas mediante gestos de la mano, detectados a través de la cámara web.

## Características
- Detección de gestos en tiempo real
- Síntesis de audio dinámica
- Piano virtual con feedback visual
- Visualizador geométrico de efectos
- Interfaz minimalista y moderna

## Requisitos
- Python 3.8+
- Webcam
- Dependencias principales:
  ```
  opencv-python
  mediapipe
  numpy
  sounddevice
  ```

## Instalación
1. Clonar el repositorio:
   ```bash
   git clone https://github.com/tuusuario/hand-music-detector.git
   cd hand-music-detector
   ```

2. Crear entorno virtual:
   ```bash
   python -m venv venv
   ```

3. Activar entorno virtual:
   - Windows:
     ```bash
     .\venv\Scripts\activate
     ```
   - Linux/Mac:
     ```bash
     source venv/bin/activate
     ```

4. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```

## Uso
1. Ejecutar el programa:
   ```bash
   python src/main.py
   ```
2. Mostrar dedos frente a la cámara:
   - 1 dedo: Do
   - 2 dedos: Re
   - 3 dedos: Mi
   - 4 dedos: Fa
   - 5 dedos: Sol
   - Puño cerrado: Silencio

3. Presionar 'q' para salir

## Melodías Disponibles
Con las 5 notas disponibles (Do, Re, Mi, Fa, Sol) se pueden tocar varias melodías populares:

### Cumpleaños Feliz
```
Notas: Do Do Re Do Fa Mi
Dedo:  1  1  2  1  4  3
Letra: Cum-ple-a-ños-Fe-liz

Notas: Do Do Re Do Sol Fa
Dedo:  1  1  2  1   5  4
Letra: Cum-ple-a-ños-Fe-liz
```

### Himno a la Alegría (Fragmento)
```
Notas: Mi Mi Fa Sol Sol Fa Mi Re Do Do Re Mi Mi Re Re
Dedo:  3  3   4  5   5  4  3  2  1  1  2  3  3  2  2
```

### La lechuza hace 'shh'
```
Notas: Do Re Mi Do | Do Re Mi Do | Mi Fa Sol | Mi Fa Sol
Dedo:  1  2  3  1  | 1  2  3  1  | 3  4  5  | 3  4  5
Letra: La-le-chu-za | La-le-chu-za | ha-ce-shh! | ha-ce-shh!
```

### Estrellita 
```
Notas: Do Do Sol Sol | Do Do Sol* (adaptado por falta de 'La')
Dedo:  1  1  5  5   | 1  1  5
Letra: Es-tre lli-ta | ¿don-de es-tas?

Notas: Fa Fa Mi Mi | Re Re Do
Dedo:  4  4  3  3  | 2  2  1
Letra: Me-pre-gun-to | quien-se-rás
```

### Guía de Interpretación
- Cada nota corresponde a una sílaba
- Los guiones (-) indican separación de sílabas

### Tips para Tocar
- Practicar primero mostrando los dedos sin música
- Seguir el ritmo natural de las palabras
- Usar el puño cerrado para silencios entre frases

## Estructura del Proyecto
```
hand-music-detector/
├── src/
│   ├── main.py            # Punto de entrada
│   ├── hand_detector.py   # Detección de gestos
│   ├── audio_player.py    # Generación de audio
│   ├── visual_effects.py  # Efectos visuales
│   └── visual_overlays.py # Elementos de UI
├── requirements.txt       # Dependencias
├── README.md           # Documentación
```

## Licencia
Este proyecto está licenciado bajo la Licencia MIT - vea el archivo [LICENSE](LICENSE) para más detalles.

La licencia MIT permite:
- ✓ Uso comercial
- ✓ Modificación
- ✓ Distribución
- ✓ Uso privado

Condiciones:
- ℹ️ Incluir copia de la licencia y copyright
- ℹ️ Uso "tal cual", sin garantías