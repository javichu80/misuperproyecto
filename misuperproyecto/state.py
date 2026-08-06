import os
import reflex as rx
from .models import Materia
import requests #Libreria para llamar  a APIs externas

class State(rx.State):
    brand_name: str = "Mi Academia STEM"
    filtro_curso: str = "Todos"
    buscar_texto: str = "" # Variable necesaria para buscador reactivo 

    #VARIABLES PARA EL TUTOR STEM CONO IA
    pregunta_tutor: str = ""
    respuesta_tutor: str = ""
    esta_cargando: bool = False
    
    # Convertimos los objetos a diccionarios al inicializar
    paquetes: list[dict] = [
        Materia("Mates Fáciles", "1º ESO", "Mates", "Dominio de EBAU.", 45.0, "calculator").to_dict(),
        Materia("Tecnologia", "2º ESO", "Naturaleza", "maquinaria industrial.", 35.0, "settings").to_dict(),
        Materia("Iniciación a la Robótica", "4º ESO", "Tecnología", "Arduino práctico.", 25.0, "cpu").to_dict(),
        Materia("Química", "2º Bachillerato", "Física", "Dominio de EBAU.", 45.0, "flask-conical").to_dict(),
        Materia("Álgebra Lineal", "1º Bachillerato", "Matemáticas", "Matrices y cálculo.", 35.0, "pi").to_dict(),
        Materia("Robótica", "4º ESO", "Automatas", "MicroBIT.", 25.0, "bot").to_dict(),
        Materia("Química", "3º ESO", "Tecnología", "Arduino práctico.", 50.0, "atom").to_dict(),    ]

    @rx.var
    def paquetes_filtrados(self) -> list[dict]:
        filtrados = self.paquetes
        
        # Filtro por curso
        if self.filtro_curso != "Todos":
            filtrados = [p for p in filtrados if p["curso"] == self.filtro_curso]
        
        # Filtro por texto de búsqueda (Innovación en UX)
        if self.buscar_texto != "":
            filtrados = [
                p for p in filtrados 
                if self.buscar_texto.lower() in p["nombre"].lower() 
                or self.buscar_texto.lower() in p["descripcion"].lower()
            ]
        
        return filtrados
    
    def set_filtro(self, valor: str):
        """ESTA ES LA FUNCIÓN QUE FALTABA: Actualiza el curso seleccionado."""
        self.filtro_curso = valor

    def set_buscar(self, valor: str):
        """Maneja el evento de cambio en la barra de busqueda"""
        self.buscar_texto = valor

    # --- LÓGICA DEL TUTOR STEM (HUGGING FACE API) ---
    def preguntar_tutor(self):
        """Envía la duda del alumno a un modelo de código abierto gratuito."""
        if not self.pregunta_tutor:
            return

        self.esta_cargando = True
        yield # Permite que Reflex actualice la UI para mostrar el estado de "Cargando" [48, Conversación previa]

        # Configuración de Hugging Face (Gratis y confiable)
        # Nota: Debes obtener un token gratuito en huggingface.co
        API_URL = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"
        token = os.getenv("HUGGINGFACE_TOKEN")
        headers = {"Authorization": "Bearer {token}"}

        payload = {
            "inputs": f"<|system|>\nEres un tutor experto en STEM. Responde de forma breve y educativa.</s>\n<|user|>\n{self.pregunta_tutor}</s>\n<|assistant|>\n",
            "parameters": {"max_new_tokens": 500}
        }

        try:
            # Petición saliente (funciona perfectamente en local sin hosting) [Conversación previa]
            response = requests.post(API_URL, headers=headers, json=payload)
            result = response.json()
            # Extraemos solo la respuesta generada
            self.respuesta_tutor = result['generated_text'].split("<|assistant|>\n")[-1]
        except Exception as e:
            self.respuesta_tutor = f"Lo siento, el tutor está descansando. Error: {str(e)}"
        
        self.esta_cargando = False