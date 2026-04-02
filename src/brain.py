import requests
import os
import json
import time
from dotenv import load_dotenv

load_dotenv()

class JobHunterBrain:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.model_id = self._descubrir_modelo_activo()
        self.url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model_id}:generateContent?key={self.api_key}"
        
        # PERFIL ESTRATÉGICO (Tu base de conocimientos para la IA)
        self.perfil_estrategico = """
        Candidata: Monica Pradines Alvarado. 
        Perfil: Ingeniera Comercial + Full Stack Developer (Santiago, Chile).
        Idiomas: Español nativo. Inglés: Básico (No postular si piden inglés fluido).
        Stack: Python, Django, PostgreSQL, Kotlin (Android), React.
        Proyectos: TaxVision (SaaS Tributario Chile/SII), Cuida$ (Finanzas), Milla Logística (GPS).
        Valor Único: Mezcla de visión de negocios, finanzas corporativas y desarrollo de software.
        """

    def _descubrir_modelo_activo(self):
        list_url = f"https://generativelanguage.googleapis.com/v1beta/models?key={self.api_key}"
        try:
            res = requests.get(list_url).json()
            for m in res.get('models', []):
                if 'generateContent' in m.get('supportedGenerationMethods', []):
                    nombre = m['name'].split('/')[-1]
                    return nombre
            return "gemini-1.5-flash"
        except Exception:
            return "gemini-1.5-flash"

    def analyze_job(self, titulo, descripcion_o_url):
        headers = {'Content-Type': 'application/json'}
        
        # PROMPT DE COPILOTO: Preparando tus argumentos para la postulación manual
        prompt = f"""
        Actúa como mi Asesor de Carrera IT. Compara mi perfil con este aviso.
        PERFIL: {self.perfil_estrategico}
        AVISO: {titulo} ({descripcion_o_url[:500]})

        INSTRUCCIONES:
        1. Evalúa el match (0-100). Si piden inglés fluido, pon 0.
        2. ARGUMENTOS: Dame 3 puntos clave de mi experiencia (TaxVision, Cuida$, Milla o Comercial) para responder preguntas del formulario.
        3. ADVERTENCIA: Dime en qué punto del aviso debo tener cuidado al responder.

        Responde ESTRICTAMENTE en JSON:
        {{
            "porcentaje": int,
            "analisis": "Resumen del match",
            "cv_adaptado": "Pitch inicial de presentación",
            "argumentos_ganadores": ["punto 1", "punto 2", "punto 3"],
            "advertencia": "Dato crítico para la postulación"
        }}
        """

        payload = {"contents": [{"parts": [{"text": prompt}]}]}

        # LÓGICA DE REINTENTO (Retry Logic)
        max_intentos = 3
        espera_429 = 60 

        for intento in range(max_intentos):
            try:
                response = requests.post(self.url, headers=headers, json=payload, timeout=30)
                
                if response.status_code == 200:
                    texto_respuesta = response.json()['candidates'][0]['content']['parts'][0]['text']
                    limpio = texto_respuesta.replace('```json', '').replace('```', '').strip()
                    return json.loads(limpio)
                
                elif response.status_code == 429:
                    print(f"⚠️ API Saturada (429). Intento {intento+1}/{max_intentos}. Esperando {espera_429}s...")
                    time.sleep(espera_429)
                    continue 
                
                else:
                    print(f"❌ Error API ({response.status_code})")
                    break

            except Exception as e:
                print(f"⚠️ Error de conexión: {e}")
                break
        
        return {
            "porcentaje": 0, 
            "analisis": "Error tras reintentos", 
            "cv_adaptado": "",
            "argumentos_ganadores": [],
            "advertencia": ""
        }