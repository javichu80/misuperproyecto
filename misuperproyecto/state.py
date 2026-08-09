import os
import reflex as rx
from .models import Materia
from dotenv import load_dotenv 

# Esta línea es la que "inyecta" tu token de Hugging Face en la memoria del programa
load_dotenv() 

class State(rx.State):
    brand_name: str = "Mi Academia STEM"
    filtro_curso: str = "Todos"
    buscar_texto: str = "" # Variable necesaria para buscador reactivo 

    # VARIABLES PARA EL TUTOR STEM COMO IA
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
        Materia("Química", "3º ESO", "Tecnología", "Arduino práctico.", 50.0, "atom").to_dict(),    
    ]

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

    def set_pregunta_tutor(self, valor: str):
        """Actualiza la variable pregunta_tutor con el texto que escribe el alumno."""
        self.pregunta_tutor = valor
    
    def set_filtro(self, valor: str):
        """Actualiza el curso seleccionado."""
        self.filtro_curso = valor

    def set_buscar(self, valor: str):
        """Maneja el evento de cambio en la barra de busqueda"""
        self.buscar_texto = valor

    # --- LÓGICA DEL TUTOR STEM OPTIMIZADA Y ASÍNCRONA ---
    async def preguntar_tutor(self):
        print(f"--- Iniciando consulta para: {self.pregunta_tutor} ---")
        if not self.pregunta_tutor:
            return

        self.esta_cargando = True
        yield  # Muestra el spinner de carga de inmediato en Reflex

        # Importamos las dependencias oficiales de Hugging Face de forma interna y asíncrona
        from huggingface_hub import AsyncInferenceClient
        import asyncio

        token = os.getenv("HUGGINGFACE_TOKEN")

        try:
            # Inicializamos el cliente asíncrono nativo para el modelo Mistral
            client = AsyncInferenceClient(
                model="deepseek-ai/DeepSeek-V4-Flash", 
                token=token
            )
            
            # Estructuramos el prompt utilizando el formato limpio de mensajes
            messages = [
                {
                    "role": "user", 
                    "content": f"Eres un tutor experto en STEM. Responde en español de forma breve. \n\n {self.pregunta_tutor}"
                }
            ]
            
            # Ejecutamos la llamada asíncrona con un tiempo límite de 15 segundos
            response = await asyncio.wait_for(
                client.chat.completions.create(
                    messages=messages,
                    max_tokens=500,
                ),
                timeout=15.0
            )
            
            # El cliente limpia automáticamente las etiquetas [/INST] y nos da el texto puro
            self.respuesta_tutor = response.choices[0].message.content

        except asyncio.TimeoutError:
            self.respuesta_tutor = "Error: El servidor de Hugging Face está tardando demasiado en responder."
        except Exception as e:
            self.respuesta_tutor = f"Error de conexión: {str(e)}"

        self.esta_cargando = False
        print(f"--- Respuesta procesada ---")
        yield  # Oculta el spinner y dibuja la respuesta en la pantalla













