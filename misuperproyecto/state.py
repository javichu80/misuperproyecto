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
    historial_chat: list[tuple[str,str]]=[]
    esta_cargando: bool = False 

    esta_autenticado: bool = False
    password_input: str = ""

    def login(self):
        """Verificación simple de credenciales."""
        # En una app real, esto consultaría una base de datos de usuarios
        if self.password_input == "admin123": # Cambia esta clave
            self.esta_autenticado = True
            self.password_input = "" # Limpiamos el campo
        else:
            return rx.window_alert("Contraseña incorrecta")

    def logout(self):
        """Cierra la sesión del administrador."""
        self.esta_autenticado = False
  
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


    def login(self):
        if self.password_input == "Cursillos":
            self.esta_autenticado = True
            self.password_input = ""
        else:
            return rx.window_alert("Contraseña incorrecta")

    # AÑADE ESTO MANUALMENTE SI FALLA EL AUTOMÁTICO
    def set_password_input(self, valor: str):
        self.password_input = valor

    
    # --- LÓGICA DEL TUTOR STEM OPTIMIZADA Y ASÍNCRONA ---
    async def preguntar_tutor(self):
        print(f"--- Iniciando consulta para: {self.pregunta_tutor} ---")
        if not self.pregunta_tutor:
            return

        # Guardamos la pregunta actual en una variable local antes de limpiar el input
        pregunta_actual = self.pregunta_tutor
        self.esta_cargando = True
        yield  # Actualiza la UI para mostrar el spinner

        from huggingface_hub import AsyncInferenceClient
        import asyncio
        import os

        token = os.getenv("HUGGINGFACE_TOKEN")

        try:
            client = AsyncInferenceClient(
                model="deepseek-ai/DeepSeek-V4-Flash", 
                token=token
            )
            
            messages = [
                {
                    "role": "user", 
                    "content": f"""Eres un tutor experto en STEM para Educación 3.0. 
                    Responde siempre usando formato Markdown profesional.
                    INSTRUCCIONES DE FORMATO:
                    1. Usa títulos (##) para separar secciones.
                    2. Usa negritas para conceptos clave.
                    3. Para las fórmulas matemáticas, usa NOTACIÓN LATEX:
                    - Si la fórmula va en su propia línea, ponla entre dobles dólares: $$ fórmula $$.
                    - Si va dentro de una frase, usa un solo dólar: $ fórmula $.
                    4. Deja siempre una línea en blanco entre párrafos.

                    PREGUNTA DEL ALUMNO: \n\n {pregunta_actual}"""
                }
            ]
            
            response = await asyncio.wait_for(
                client.chat.completions.create(
                    messages=messages,
                    max_tokens=500,
                ),
                timeout=15.0
            )
            
            # 1. Capturamos la respuesta en una variable local
            respuesta_ia = response.choices[0].message.content

        except asyncio.TimeoutError:
            respuesta_ia = "Error: El servidor de Hugging Face está tardando demasiado en responder."
        except Exception as e:
            respuesta_ia = f"Error de conexión: {str(e)}"

        # 2. AÑADIMOS LA INTERACCIÓN AL HISTORIAL (El cambio más importante)
        # Esto añade una tupla (pregunta, respuesta) a tu lista
        self.historial_chat.append((pregunta_actual, respuesta_ia))

        # 3. LIMPIAMOS EL INPUT para la siguiente pregunta
        self.pregunta_tutor = ""
        
        self.esta_cargando = False
        print(f"--- Respuesta añadida al historial ---")
        yield 


