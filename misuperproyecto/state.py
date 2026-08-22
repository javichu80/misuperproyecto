import os
import reflex as rx
import yaml
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

 # --- NUEVO: Estado de Navegación del Blueprint ---
    selected_course: str = "matematicas_1eso"
    selected_topic: str = "tema_01_numeros_naturales"
    selected_lesson: str = "lesson_01_sistemas_numeracion"
    lesson_content: str = ""
    
    # Guardamos como lista de listas [lesson_id, title] para evitar fallos de bindings
    lessons_list: list[list[str]] = []

    def cargar_estructura_lecciones(self):
        """Lee metadata.yaml y carga la lista de lecciones del Tema 1 en el Estado."""

        metadata_path = (
            f"courses/{self.selected_course}/"
            f"{self.selected_topic}/metadata.yaml"
        )

        # DEBUG
        print("METADATA:", metadata_path)
        print("EXISTE:", os.path.exists(metadata_path))

        if os.path.exists(metadata_path):
            try:
                with open(metadata_path, "r", encoding="utf-8") as f:
                    data = yaml.safe_load(f)

                    lessons = data.get("lessons", [])

                    self.lessons_list = [
                        [l.get("lesson_id"), l.get("title")]
                        for l in lessons
                    ]

                    # DEBUG
                    print("LESSONS:", self.lessons_list)

            except Exception as e:
                print(f"Error cargando metadatos: {e}")

        self.cargar_contenido_leccion(self.selected_lesson)

    def cargar_contenido_leccion(self, lesson_id: str):
        """Cambia la lección activa y lee el archivo Markdown correspondiente."""
        self.selected_lesson = lesson_id
        
        # Buscamos el nombre del archivo .md asociado en metadata.yaml
        lesson_file = "lesson_01.md"  # valor por defecto de seguridad
        metadata_path = f"courses/{self.selected_course}/{self.selected_topic}/metadata.yaml"
        
        if os.path.exists(metadata_path):
            with open(metadata_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
                for l in data.get("lessons", []):
                    if l.get("lesson_id") == lesson_id:
                        lesson_file = l.get("file")
                        break

        # Leemos el archivo Markdown
        file_path = f"courses/{self.selected_course}/{self.selected_topic}/{lesson_file}"
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                self.lesson_content = f.read()
        else:
            self.lesson_content = f"# Error\nNo se pudo encontrar el archivo de teoría: `{lesson_file}`."

    # --- NUEVA FUNCIÓN ON_LOAD COMBINADA ---
    def iniciar_pagina(self):
        """Inicializa tanto la base de datos de materias como el cargador de Markdown."""
        self.cargar_materias()  # Tu función existente de carga de DB
        self.cargar_estructura_lecciones()  # Nuestra nueva función de carga de archivos





    esta_autenticado: bool = False
    # ¡HEMOS ELIMINADO 'password_input' de aquí para evitar colisiones!

    def login(self, form_data: dict):
        """Verificación segura mediante formulario."""
        # IMPRIMIMOS EN TU TERMINAL PARA MONITOREAR LA ENTRADA
        print("\n=== DEBUG LOGIN ACADEMA ===")
        print(f"Diccionario recibido del formulario: {form_data}")
        
        # Recuperamos la clave usando el nuevo nombre 'password_field'
        password_ingresado = form_data.get("password_field", "").strip()
        
        print(f"Contraseña extraída y limpia: '{password_ingresado}'")
        print("============================\n")

        if password_ingresado == "Cursos": 
            self.esta_autenticado = True
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


