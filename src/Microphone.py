import queue
import speech_recognition as sr
from typing import Optional
class Microphone:
    def __init__(self):
        self.audio_queue = queue.Queue()
        self.recognizer = sr.Recognizer()
    
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