import requests
import json
class Comunication():
    def __init__(self):
        self.url='http://localhost:1234/v1/chat/completions'
        self.historial = [
            {"role": "system", "content": """IMPORTANTE: 
             Sigue estas reglas estrictamente: 
             1. Responde siempre en una sola línea sin saltos. 
             2. No uses ningún tipo de decorador o formato. 
             3. No uses expresiones como 'te explico', 
             'déjame decirte', etc. 4. No uses emojis ni símbolos 
             especiales. 5. Limita tu respuesta a máximo 5 líneas 
             cortas. 6. No des introducciones ni conclusiones. 
             7. Ve directo al punto. 8. Si la pregunta requiere una 
             respuesta más larga, menciona solo los puntos más 
             importantes."""
             }
        ]
        self._comunication = None

    def set_comunication(self, comunication):
        self._comunication = comunication

    def send_message(self, message):
        self._comunication.send_message(message)

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
            print(resultado)
            texto_respuesta = resultado['choices'][0]['message']['content']
            
            self.historial.extend([
                {"role": "user", "content": entrada},
                {"role": "assistant", "content": texto_respuesta}
            ])
            
            return texto_respuesta

        except Exception as e:
            return f"Error: {str(e)}"