import pyttsx3
class Speaker():
    def __init__(self):
        self.engine = pyttsx3.init()
        voices = self.engine.getProperty('voices')
        for voice in voices:
            print(voice)    
            if "spanish" in voice.id.lower():
                self.engine.setProperty('voice', voice.id)

    def speak(self, texto: str):
        self.engine.say(texto)
        self.engine.runAndWait()
    
    