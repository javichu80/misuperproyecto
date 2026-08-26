import os
import yaml
import reflex as rx
import ollama
import httpx
from .models import Materia
from dotenv import load_dotenv
from sqlmodel import select
from dataclasses import dataclass

load_dotenv()

# =========================================================================
# MOLDES DE DATOS (EXIGIDOS EN REFLEX 0.9.X PARA EVITAR ERRORES DE REACT)
# =========================================================================
@dataclass
class Lesson:
    lesson_id: str
    title: str

class State(rx.State):
    # =========================================================================
    # VARIABLES DE UI, AUTENTICACIÓN Y FILTROS
    # =========================================================================
    brand_name: str = "Mi Academia STEM"
    filtro_curso: str = "Todos"
    buscar_texto: str = ""
    esta_autenticado: bool = False
    
    # Inputs del formulario para crear materias
    nuevo_nombre: str = ""
    nuevo_curso: str = ""
    nuevo_categoria: str = ""
    nueva_descripcion: str = ""
    nuevo_precio: int = 0
    nuevo_icono: str = "book-open"

    # Base de datos local
    materias: list[Materia] = []

    # =========================================================================
    # VARIABLES DE IA GENÉRICA (DEEPSEEK - CONSULTA GLOBAL)
    # =========================================================================
    historial_chat: list[tuple[str, str]] = []
    pregunta_tutor: str = ""
    esta_cargando: bool = False

    # =========================================================================
    # VARIABLES DE IA DE ESTUDIO (GEMMA - CONTEXTO LECCIÓN)
    # =========================================================================
    historial_leccion: list[tuple[str, str]] = []
    pregunta_leccion: str = ""
    cargando_leccion: bool = False

    # Navegación del Blueprint pedagógico
    selected_course: str = "matematicas_1eso"
    selected_topic: str = "tema_01_numeros_naturales"
    selected_lesson: str = "lesson_01_sistemas_numeracion"
    lesson_content: str = ""
    
    # Lista de lecciones tipada para el compilador
    lessons_list: list[Lesson] = []

    # --- VARIABLES DE ACTIVIDAD Y PROGRESO (SPRINT 3) ---
    respuesta_alumno: str = ""           # Captura el texto del formulario de entrega
    correccion_tutor: str = ""           # Almacena el feedback constructivo de Gemma
    cargando_correccion: bool = False    # Controla el spinner del botón de entrega
    ultimo_resultado_correcto: bool = False  # Para dar estilo verde (correcto) o marrón (repasar)
    lecciones_completadas: list[str] = [] # Almacena las IDs de las lecciones resueltas con éxito
    progreso: int = 0                    # Porcentaje total de progreso (0 a 100)


    # =========================================================================
    # SETTERS EXPLÍCITOS (REQUISITO FUNDAMENTAL PARA REFLEX v0.9.X)
    # =========================================================================
    def set_filtro_curso(self, valor: str):
        self.filtro_curso = valor

    def set_buscar_texto(self, valor: str):
        self.buscar_texto = valor

    def set_nuevo_nombre(self, valor: str):
        self.nuevo_nombre = valor

    def set_nuevo_curso(self, valor: str):
        self.nuevo_curso = valor

    def set_nuevo_categoria(self, valor: str):
        self.nuevo_categoria = valor

    def set_nueva_descripcion(self, valor: str):
        self.nueva_descripcion = valor

    def set_nuevo_precio(self, valor: str):
        try:
            self.nuevo_precio = int(valor) if valor else 0
        except ValueError:
            self.nuevo_precio = 0

    def set_pregunta_leccion(self, valor: str):
        self.pregunta_leccion = valor

    def set_pregunta_tutor(self, valor: str):
        self.pregunta_tutor = valor

    def set_respuesta_alumno(self, val: str):
        """Setter explícito para evitar problemas de compilación en caliente."""
        self.respuesta_alumno = val

    # =========================================================================
    # EVENTOS DE NAVEGACIÓN Y CARGA DE CONTENIDOS
    # =========================================================================
    def cargar_estructura_lecciones(self):
        """Lee metadata.yaml y carga la lista de lecciones del Tema 1."""
        metadata_path = f"courses/{self.selected_course}/{self.selected_topic}/metadata.yaml"
        if os.path.exists(metadata_path):
            try:
                with open(metadata_path, "r", encoding="utf-8") as f:
                    data = yaml.safe_load(f)
                    lessons = data.get("lessons", [])
                    self.lessons_list = [
                        Lesson(lesson_id=l.get("lesson_id"), title=l.get("title"))
                        for l in lessons
                    ]
            except Exception as e:
                print(f"Error cargando metadatos: {e}")
        
        self.cargar_contenido_leccion(self.selected_lesson)

    def cargar_contenido_leccion(self, lesson_id: str):
        """Cambia la lección activa y lee el archivo Markdown correspondiente."""
        self.selected_lesson = lesson_id
        lesson_file = "lesson_01.md"
        metadata_path = f"courses/{self.selected_course}/{self.selected_topic}/metadata.yaml"
        
        if os.path.exists(metadata_path):
            with open(metadata_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
                for l in data.get("lessons", []):
                    if l.get("lesson_id") == lesson_id:
                        lesson_file = l.get("file")
                        break

        file_path = f"courses/{self.selected_course}/{self.selected_topic}/{lesson_file}"
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                self.lesson_content = f.read()
            self.historial_leccion = []
        else:
            self.lesson_content = f"# Error\nNo se pudo encontrar el archivo de teoría: `{lesson_file}`."

    # =========================================================================
    # EVENTO ON_LOAD COORDINADOR
    # =========================================================================
    def iniciar_pagina(self):
        """Inicializa tanto la base de datos de SQLModel como el cargador de Markdown."""
        self.cargar_materias()
        self.cargar_estructura_lecciones()

    def cargar_materias(self):
        """Carga todas las materias existentes en la base de datos."""
        with rx.session() as session:
            self.materias = session.exec(select(Materia)).all()

    # =========================================================================
    # LÓGICA DE GESTIÓN DE MATERIAS (CRUD)
    # =========================================================================
    def guardar_materia(self):
        """Añade una nueva materia al catálogo de la base de datos."""
        with rx.session() as session:
            nueva = Materia(
                nombre=self.nuevo_nombre,
                curso=self.nuevo_curso,
                categoria=self.nuevo_categoria,
                descripcion=self.nueva_descripcion,
                precio=self.nuevo_precio,
                icono=self.nuevo_icono
            )
            session.add(nueva)
            session.commit()
            
        # Reseteamos inputs
        self.nuevo_nombre = ""
        self.nuevo_curso = ""
        self.nuevo_categoria = ""
        self.nueva_descripcion = ""
        self.nuevo_precio = 0
        self.cargar_materias()

    def borrar_materia(self, id_materia: int):
        """Elimina una materia de la base de datos por su ID."""
        with rx.session() as session:
            materia = session.get(Materia, id_materia)
            if materia:
                session.delete(materia)
                session.commit()
        self.cargar_materias()

    @rx.var
    def materias_filtradas(self) -> list[Materia]:
        """Devuelve las materias filtradas según el curso y el buscador superior."""
        resultado = self.materias
        if self.filtro_curso != "Todos":
            resultado = [m for m in resultado if m.curso == self.filtro_curso]
        if self.buscar_texto.strip():
            texto = self.buscar_texto.lower().strip()
            resultado = [
                m for m in resultado 
                if texto in m.nombre.lower() or texto in m.descripcion.lower()
            ]
        return resultado

    # =========================================================================
    # LÓGICA DE AUTENTICACIÓN
    # =========================================================================
    def login(self, password_dict: dict):
        """Valida la contraseña y abre el panel principal."""
        password_ingresado = password_dict.get("password_field", "").strip()
        print("=== DEBUG LOGIN ACADEMA ===")
        print(f"Diccionario recibido del formulario: {password_dict}")
        print(f"Contraseña extraída y limpia: '{password_ingresado}'")
        print("============================")
        
        if password_ingresado == "Cursillos":
            self.esta_autenticado = True
        else:
            return rx.window_alert("Contraseña incorrecta")

    def logout(self):
        """Cierra la sesión de usuario de forma limpia."""
        self.esta_autenticado = False

    # =========================================================================
    # LÓGICA CHAT 1: TUTOR DE LECCIÓN CONTEXTUAL (OLLAMA LOCAL)
    # =========================================================================
    async def preguntar_tutor_leccion(self):
        """Inyecta la teoría en Gemma (Ollama) para guiar socráticamente al alumno."""
        if not self.pregunta_leccion.strip():
            return

        pregunta_alumno = self.pregunta_leccion.strip()
        # Limpiamos el cuadro de texto de la lección inmediatamente para mejorar la experiencia de usuario
        self.pregunta_leccion = ""
        self.cargando_leccion = True
        yield

        # 1. Definimos las instrucciones de rol y comportamiento socrático
        system_prompt = (
            "Eres un tutor de Inteligencia Artificial especializado en STEM para alumnos de 1º de ESO. "
            "Tu objetivo es guiar al estudiante de manera socrática, explicándole paso a paso sin darle la solución directa, "
            "haciendo preguntas de control y usando ejemplos cotidianos para facilitar la comprensión.\n"
            "Sigue estas reglas estrictas de conducta pedagógica:\n"
            "1. NUNCA le des la solución directa de los ejercicios o actividades al alumno. "
            "Si te pide un resultado, ofrécele pistas, hazle preguntas guía o divide el problema en partes más sencillas para que él descubra la solución.\n"
            "2. Si el alumno te pregunta algo fuera de tema o del contexto de la lección activa (como preguntas genéricas sobre la Luna), "
            "busca una relación creativa o divertida para reconducir la conversación hacia las matemáticas o hacia el tema de la lección activa."
        )

        # 2. Inyectamos dinámicamente el contenido Markdown de la lección que el alumno está estudiando
        contexto_leccion = (
            f"El alumno está estudiando actualmente la lección:\n"
            f"=== CONTENIDO DE LA LECCIÓN ===\n"
            f"{self.lesson_content}\n"
            f"================================\n\n"
            f"Responde de forma guiada apoyándote estrictamente en este contenido teórico."
            f"y aplicando de forma rigurosa tus pautas de profesor socrático."
        )

        messages_api = [
            {"role": "system", "content": f"{system_prompt}\n\n{contexto_leccion}"}
        ]

        # 3. CONTEXTO SEGURO: Añadimos el historial reciente ANTES de meter el "Pensando..."
        for prev_preg, prev_resp in self.historial_leccion[-3:]:
            messages_api.append({"role": "user", "content": prev_preg})
            messages_api.append({"role": "assistant", "content": prev_resp})

        # Añadimos la pregunta actual del alumno al mensaje de la API
        messages_api.append({"role": "user", "content": pregunta_alumno})

        # 4. UX INSTANTÁNEA: Mostramos la pregunta y el globo "Pensando..." en la pantalla inmediatamente
        self.historial_leccion = self.historial_leccion + [(pregunta_alumno, "Pensando...")]
        yield

        # 5. LLAMADA ASÍNCRONA A OLLAMA
        try:
            response = await ollama.AsyncClient().chat(
                model="gemma2:2b",
                messages=messages_api,
            )
            respuesta_gemma = response["message"]["content"]
            
            # Reemplazamos quirúrgicamente el "Pensando..." por la respuesta final estructurada de Gemma
            self.historial_leccion = self.historial_leccion[:-1] + [(pregunta_alumno, respuesta_gemma)]
        except Exception as e:
            error_msg = "⚠️ No he podido conectar con Gemma local. Comprueba que Ollama está activo (`ollama run gemma`)."
            # Si falla, reemplazamos el "Pensando..." por el mensaje de error amigable
            self.historial_leccion = self.historial_leccion[:-1] + [(pregunta_alumno, error_msg)]
            print(f"Error en Ollama: {e}")

        self.cargando_leccion = False
        yield

    # =========================================================================
    # LÓGICA ACTIVIDAD: CORRECCIÓN DE EJERCICIOS Y PROGRESO (OLLAMA LOCAL)
    # =========================================================================
    async def corregir_actividad(self):
        """Envía la respuesta del ejercicio a Gemma para que la evalúe pedagógicamente."""
        if not self.respuesta_alumno.strip():
            return

        self.cargando_correccion = True
        yield

        # 1. Indicamos a Gemma su rol como evaluador socrático y empático
        system_prompt = (
            "Eres un evaluador pedagógico de matemáticas para alumnos de 1º de ESO. "
            "Tu única tarea es corregir la respuesta del alumno para la sección 'Actividad' de la lección.\n\n"
            "REGLAS CRÍTICAS DE EVALUACIÓN:\n"
            "1. Identifica qué ejercicio está intentando responder el alumno. Ignora si el alumno se equivoca al escribir el número del ejercicio (por ejemplo, si escribe 'ejercicio 2' pero da una respuesta en números romanos, asume de inmediato que está respondiendo al ejercicio de números romanos de la lección).\n"
            "2. Compara el valor matemático de la respuesta con la teoría. Ten en cuenta que para el número 3.456, la conversión a romano correcta es exactamente 'MMMCDLVI' (o en minúsculas 'mmmcdlvi'). Si el alumno ha escrito eso, la respuesta es 100% CORRECTA.\n"
            "3. Sé flexible con el formato de la frase del alumno. Lo importante es que el resultado final del cálculo o de la conversión sea matemáticamente correcto.\n"
            "4. Dale un feedback breve, empático y muy animador en caso de éxito. Si comete un error real, ofrécele una pista sutil sin darle la solución.\n"
            "5. Al final de tu mensaje, en una nueva línea limpia, debes escribir obligatoriamente una de estas dos etiquetas:\n"
            "   - Si la resolución es matemáticamente correcta: '[RESULTADO: CORRECTO]'\n"
            "   - Si tiene fallos reales o está incompleto: '[RESULTADO: REPASAR]'"
        )

        contexto_leccion = (
            f"=== CONTENIDO DE LA LECCIÓN ===\n"
            f"{self.lesson_content}\n"
            f"================================\n\n"
            f"Respuesta enviada por el alumno:\n"
            f"\"{self.respuesta_alumno}\""
        )

        try:
            # Llamada asíncrona a tu gemma2:2b local
            response = await ollama.AsyncClient().chat(
                model="gemma2:2b",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": contexto_leccion}
                ]
            )
            feedback = response["message"]["content"]

            # 2. Procesamos el veredicto de Gemma para actualizar el estado
            if "[RESULTADO: CORRECTO]" in feedback:
                self.ultimo_resultado_correcto = True
                # Limpiamos la etiqueta técnica de la respuesta final que lee el alumno
                self.correccion_tutor = feedback.replace("[RESULTADO: CORRECTO]", "").strip()
                
                # Si es correcto y no estaba completada, la añadimos al progreso
                if self.selected_lesson not in self.lecciones_completadas:
                    self.lecciones_completadas.append(self.selected_lesson)
            else:
                self.ultimo_resultado_correcto = False
                self.correccion_tutor = feedback.replace("[RESULTADO: REPASAR]", "").strip()

            # 3. Calculamos dinámicamente el progreso sobre la lista de lecciones del Tema 1
            if self.lessons_list:
                self.progreso = int((len(self.lecciones_completadas) / len(self.lessons_list)) * 100)

        except Exception as e:
            self.correccion_tutor = "⚠️ No he podido conectar con el corrector de Ollama. Asegúrate de que está activo."
            print(f"Error en corrector: {e}")

        self.cargando_correccion = False
        yield





    # =========================================================================
    # LÓGICA CHAT 2: ASISTENTE STEM GENERAL (QWEN 2.5 - CONSULTA GLOBAL)
    # =========================================================================
    
    async def preguntar_tutor(self):
        """Chat genérico global conectado a Hugging Face usando formato compatible con OpenAI."""
        if not self.pregunta_tutor.strip():
            return
        
        pregunta = self.pregunta_tutor.strip()
        # MEJORA: Limpiamos el cuadro de texto inmediatamente para mejorar la experiencia de usuario
        self.pregunta_tutor = ""
        self.esta_cargando = True
        yield
        
        # Insertamos un estado de "Pensando..." temporal asociado a la pregunta en el historial
        self.historial_chat = self.historial_chat + [(pregunta, "Pensando...")]
        yield
        
        try:
            # Extraemos tu token de Hugging Face desde el archivo .env
            api_key = os.getenv("HUGGINGFACE_TOKEN")
            if api_key:
                async with httpx.AsyncClient() as client:
                    # Hacemos la petición al endpoint oficial de Hugging Face compatible con OpenAI
                    response = await client.post(
                        "https://router.huggingface.co/v1/chat/completions",
                        headers={
                            "Authorization": f"Bearer {api_key}",
                            "Content-Type": "application/json"
                        },
                        json={
                            # Qwen 2.5 72B es uno de los mejores y más rápidos modelos STEM en Hugging Face
                            "model": "Qwen/Qwen2.5-72B-Instruct",
                            "messages": [
                                {"role": "system", "content": "Eres un tutor STEM experto, motivador y muy pedagógico."},
                                {"role": "user", "content": pregunta}
                            ],
                            "max_tokens": 500
                        },
                        timeout=30.0
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        # ¡Al ser compatible con OpenAI, ahora sí contiene la clave 'choices' perfectamente!
                        respuesta = data["choices"][0]["message"]["content"]
                    else:
                        try:
                            error_info = response.json()
                            msg_error = error_info.get("error", {}).get("message", "Error de API")
                            # Si Hugging Face está arrancando el modelo en su servidor gratuito:
                            if "estimated_time" in error_info:
                                msg_error = "El modelo gratuito de Hugging Face se está cargando. Por favor, reenvía el mensaje en 30 segundos."
                        except Exception:
                            msg_error = f"Código de estado {response.status_code}"
                        
                        respuesta = f"⚠️ Error en Hugging Face: {msg_error}"
            else:
                respuesta = "⚠️ No se ha encontrado la variable 'HUGGINGFACE_TOKEN' en tu archivo .env."
            
            # Reemplazamos el estado de "Pensando..." por la respuesta final de Hugging Face
            self.historial_chat = self.historial_chat[:-1] + [(pregunta, respuesta)]
        except Exception as e:
            self.historial_chat = self.historial_chat[:-1] + [(pregunta, f"⚠️ Error al conectar con Hugging Face: {str(e)}")]
        
        self.esta_cargando = False
        yield
    
    