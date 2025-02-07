import threading
from src.Speaker import Speaker
from src.Comunication import Comunication
from src.Microphone import Microphone
from src.Mouse import Mouse

class AsistenteVirtual:
    def __init__(self):
        
        self.engine = Speaker()
        self.api=Comunication()
        self.microphone = Microphone()
        self.mouse = Mouse(grabarAudio=self.microphone.grabar_audio)
        
    def iniciarModel(self):
        print("Asistente Virtual: ¡Qué onda! Mantén presionado el botón del scroll para hablar (di 'salir' para terminar)")
        self.engine.speak("¡Qué onda! Presiona el botón del scroll para hablar conmigo")
        
        
        mouse_thread = threading.Thread(target=self.mouse.escuchar_evento_raton)
        mouse_thread.daemon = True
        mouse_thread.start()
        
        try:
            while True:
                entrada = self.microphone.procesar_audio()
                
                if entrada:
                    if entrada.lower() == 'salir':
                        mensaje_despedida = "¡Nos vemos!"
                        print("\nAsistente Virtual:", mensaje_despedida)
                        self.engine.speak(mensaje_despedida)
                        break
                    
                    respuesta = self.api.responder(entrada)
                    print("\nAsistente Virtual:", respuesta)
                    self.engine.speak(respuesta)
        finally:
            self.running = False  