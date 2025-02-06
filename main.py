import requests
import json
import speech_recognition as sr
import pyttsx3
from typing import Optional
from pynput import keyboard
import threading
import queue

class AsistenteVirtual:
    def __init__(self, url='http://localhost:1234/v1/chat/completions'):
        self.url = url
        self.historial = [
            {"role": "system", "content": "IMPORTANTE: Sigue estas reglas estrictamente: 1. Responde siempre en una sola línea sin saltos. 2. No uses ningún tipo de decorador o formato. 3. No uses expresiones como 'te explico', 'déjame decirte', etc. 4. No uses emojis ni símbolos especiales. 5. Limita tu respuesta a máximo 5 líneas cortas. 6. No des introducciones ni conclusiones. 7. Ve directo al punto. 8. Si la pregunta requiere una respuesta más larga, menciona solo los puntos más importantes."}
        ]
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        voices = self.engine.getProperty('voices')
        for voice in voices:
            print(voice)    
            if "spanish" in voice.id.lower():
                self.engine.setProperty('voice', voice.id)
        self.is_listening = False
        self.audio_queue = queue.Queue()
        
    def escuchar_evento_tecla(self):
        def on_press(key):
            if hasattr(key, 'char') and key.char == 'p':
                if not self.is_listening:
                    self.is_listening = True
                    print("\nGrabando... (suelta 'p' para detener)")
                    self.grabar_audio()

        def on_release(key):
            if hasattr(key, 'char') and key.char == 'p':
                self.is_listening = False
                
        with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()

    def grabar_audio(self):
        with sr.Microphone() as source:
            try:
                audio = self.recognizer.listen(source, timeout=None)
                self.audio_queue.put(audio)
            except sr.WaitTimeoutError:
                pass

    def procesar_audio(self) -> Optional[str]:
        try:
            audio = self.audio_queue.get_nowait()
            texto = self.recognizer.recognize_google(audio, language="es-MX")
            print(f"\nHas dicho: {texto}")
            return texto
        except queue.Empty:
            return None
        except sr.UnknownValueError:
            print("\nNo pude entender el audio")
            return None
        except sr.RequestError as e:
            print(f"\nError en el servicio de reconocimiento: {e}")
            return None

    def hablar(self, texto: str):
        self.engine.say(texto)
        self.engine.runAndWait()

    def responder(self, entrada):
        payload = {
            "messages": self.historial + [
                {"role": "user", "content": entrada}
            ],
            "temperature": 0.7,
            "max_tokens": 300
        }

        try:
            respuesta = requests.post(
                self.url, 
                headers={'Content-Type': 'application/json'},
                data=json.dumps(payload)
            )
            
            resultado = respuesta.json()
            texto_respuesta = resultado['choices'][0]['message']['content']
            
            self.historial.extend([
                {"role": "user", "content": entrada},
                {"role": "assistant", "content": texto_respuesta}
            ])
            
            return texto_respuesta

        except Exception as e:
            return f"Error: {str(e)}"

def main():
    asistente = AsistenteVirtual()
    print("Asistente Virtual: ¡Qué onda! Mantén presionada la tecla 'p' para hablar (di 'salir' para terminar)")
    asistente.hablar("¡Qué onda! Presiona p para hablar conmigo")
    
    # Iniciar thread para escuchar eventos del teclado
    keyboard_thread = threading.Thread(target=asistente.escuchar_evento_tecla)
    keyboard_thread.daemon = True
    keyboard_thread.start()
    
    while True:
        entrada = asistente.procesar_audio()
        
        if entrada:
            if entrada.lower() == 'salir':
                mensaje_despedida = "¡Nos vemos!"
                print("\nAsistente Virtual:", mensaje_despedida)
                asistente.hablar(mensaje_despedida)
                break
            
            respuesta = asistente.responder(entrada)
            print("\nAsistente Virtual:", respuesta)
            asistente.hablar(respuesta)

if __name__ == "__main__":
    main()