import requests
import json
class Comunication():
    def __init__(self):
        self.url='http://localhost:1234/v1/chat/completions'
        self.historial = [{
        "role": "system",
        "content": """IMPORTANTE: Sigue estas reglas estrictamente:  
        1. Responde siempre en una sola línea sin saltos.  
        2. No uses decoradores, formato especial, emojis ni símbolos.  
        3. Evita expresiones como 'te explico', 'déjame decirte', etc.  
        4. Limita tu respuesta a un máximo de 5 líneas cortas.  
        5. No des introducciones ni conclusiones, ve directo al punto.  
        6. Si la pregunta requiere una respuesta extensa, menciona solo los puntos clave.  
        7. Si preguntan qué es Audacia? o si te piden que hables sobre audacia, responde basado en: "Somos el primer centro de inteligencia artificial y robótica de excelencia para las Américas, reconocido por la OEA", sin repetirlo tal cual.  
        8. Si preguntan por patentes de Audacia, responde basado en: "Tenemos 4 patentes otorgadas y 27 en examen de fondo", sin repetirlo tal cual.  
        9. Si solicitan más información sobre Audacia, menciona: 'Contamos con más de 20 publicaciones de alto impacto, más de 30 investigadores activos y más de 300 desarrollos implementados.' """
    }]

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