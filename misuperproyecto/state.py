import os
import reflex as rx
from .models import Materia
from dotenv import load_dotenv
from sqlmodel import select

load_dotenv()

class State(rx.State):
    # Variables de UI básica
    brand_name: str = "Mi Academia STEM"
    filtro_curso: str = "Todos"
    buscar_texto: str = ""
    # Variables para el Formulario (ESTO CORRIGE TU ERROR)
    nuevo_nombre: str = ""
    nuevo_curso: str = "1º ESO"
    nueva_categoria: str = "Matemáticas"
    nueva_descripcion: str = ""
    nuevo_precio: int = 0
    nuevo_icono: str = "book-open"

    
    # Lista para las tarjetas (Vital para index)
    lista_materias: list[Materia] = []

    

    # Variables para la IA
    pregunta_tutor: str = ""
    respuesta_tutor: str = ""
    esta_cargando: bool = False 

  
    def cargar_materias(self):
        """Consulta la base de datos y la puebla si está vacía."""
        with rx.session() as session:
            materias_db = session.exec(select(Materia)).all()
            if not materias_db:
                iniciales = [
                    Materia(nombre="Próximamente NUEVAS MATERIAS", curso="Diferentes cursos", categoria="Diversas categorías", 
                            descripcion="Descúbrelas.", precio=0, icono="atom"),
                ]
                for m in iniciales:
                    session.add(m)
                session.commit()
                self.lista_materias = session.exec(select(Materia)).all()
            else:
                self.lista_materias = materias_db
    
    def guardar_materia(self):
        """Guarda la materia del formulario."""
        with rx.session() as session:
            nueva = Materia(
                nombre=self.nuevo_nombre, curso=self.nuevo_curso,
                categoria=self.nueva_categoria, descripcion=self.nueva_descripcion,
                precio=self.nuevo_precio, icono=self.nuevo_icono
            )
            session.add(nueva)
            session.commit()
            self.nuevo_nombre = "" # Limpiar
            self.cargar_materias() # Actualizar lista

    @rx.var

    def materias_filtradas(self) -> list[Materia]:

        materias = self.lista_materias

        if self.filtro_curso != "Todos":
            materias = [m for m in materias if m.curso == self.filtro_curso]

        if self.buscar_texto != "":
            materias = [m for m in materias if self.buscar_texto.lower() in m.nombre.lower()]
        return materias

    
    def set_pregunta_tutor(self, valor: str):
        """Actualiza la variable pregunta_tutor con el texto que escribe el alumno."""
        self.pregunta_tutor = valor
    
    def set_filtro(self, valor: str):
        """Actualiza el curso seleccionado."""
        self.filtro_curso = valor

    def set_buscar(self, valor: str):
        """Maneja el evento de cambio en la barra de busqueda"""
        self.buscar_texto = valor


    #FUNCIONES PARA CREAR Y BORRAR TARJETAS

    def set_nuevo_nombre(self, valor: str):
        self.nuevo_nombre = valor

    def set_nuevo_curso(self, valor: str):
        self.nuevo_curso = valor

    def set_nueva_descripcion(self, valor: str):
        self.nueva_descripcion = valor

    def set_nuevo_precio(self, valor: str): # Cambiamos int por str
        """Recibe el texto del input y lo convierte a entero de forma segura."""
        try:
            # Intentamos transformar el texto a número entero
            self.nuevo_precio = int(valor) 
        except ValueError:
            # Si el texto está vacío o no es un número, ponemos 0 para evitar el error [8, 9]
            self.nuevo_precio = 0

    def borrar_materia(self, id: int):
        """Elimina una materia por su ID y refresca la lista."""
        with rx.session() as session:
            # Buscamos la materia exacta en la base de datos usando su ID
            materia = session.get(Materia, id)
            if materia:
                session.delete(materia)
                session.commit()
        # Llamamos a cargar_materias para que la lista de la web se actualice al instante
        self.cargar_materias() 

    
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






