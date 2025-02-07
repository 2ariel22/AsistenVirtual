import win32api
import time

class Mouse():
    def __init__(self,grabarAudio):
        self.name = 'Mouse'
        self.running = True
        self.is_listening = False
        self.grabar_audio=grabarAudio
        
    def escuchar_evento_raton(self):
        MIDDLE_BUTTON = 0x04  
        while self.running:
            if win32api.GetKeyState(MIDDLE_BUTTON) < 0:  
                if not self.is_listening:
                    self.is_listening = True
                    print("\nGrabando... (suelta el botón del scroll para detener)")
                    self.grabar_audio()
            else:
                self.is_listening = False
            time.sleep(0.1) 


    def run(self):
        print(f'{self.name} is running')