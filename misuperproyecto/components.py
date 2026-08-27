import reflex as rx
from rxconfig import config
from .state import State
from .models import Materia
from .styles import estilo_base_tarjeta, estilo_boton_compra, COLOR_PRIMARIO, COLOR_BRANDNAME, COLOR_BORDE, COLOR_PANEL

# =========================================================================
# COMPONENTE 1: NAVBAR SUPERIOR INTEGRADO
# =========================================================================
def navbar() -> rx.Component:
    """Barra de navegación responsiva de Javi con enlaces y botones de filtrado."""
    return rx.flex(
        # 1. LOGO Y CABECERA (Se alinea al centro en móvil y a la izquierda en PC)
        rx.hstack(
            rx.icon(tag="graduation-cap", size=28, color="white"),
            rx.heading(State.brand_name, size="6", color=COLOR_BRANDNAME),
            spacing="3",
            align_items="center"
        ),
        
        # 2. FILTRADO DE CURSOS (Elástico: se adapta y centra si la pantalla es pequeña)
        rx.flex(
            rx.button("Todos", on_click=lambda: State.set_filtro_curso("Todos"), variant="ghost", color="white"),
            rx.button("1º ESO", on_click=lambda: State.set_filtro_curso("1º ESO"), variant="ghost", color="white"),
            rx.button("2º ESO", on_click=lambda: State.set_filtro_curso("2º ESO"), variant="ghost", color="white"),
            spacing="3",
            flex_wrap="wrap",
            justify="center",
            align_items="center",
            margin_y=["0.6em", "0"], # Margen vertical de separación solo en móviles
        ),
        
        # 3. ENLACES DE NAVEGACIÓN
        rx.hstack(
            rx.link("Inicio", href="/", color="white", underline="none"),
            rx.link("Productos", href="/productos", color="white", underline="none"),
            spacing="4",
            align_items="center"
        ),
        
        # PROPIEDADES RESPONSIVAS CLAVE PARA EL CONTENEDOR:
        flex_direction=["column", "row"],  # En columna en móvil, en fila en PC
        justify_content="space-between",   # Distribuye los 3 bloques a lo largo de la pantalla
        align_items="center",              # Centra los elementos verticalmente
        flex_wrap="wrap",                  # Permite saltos de línea fluidos si es necesario
        padding=["1em", "1em 2em"],        # Menos padding lateral en móvil para ganar espacio
        border_bottom=f"1px solid {rx.color('slate', 4)}",
        background="#000000",              # Mantenemos tu elegante negro de fondo
        width="100%",
    )

# =========================================================================
# COMPONENTE 2: SIDEBAR DE TEMARIOS REACITVO
# =========================================================================
def sidebar_lecciones() -> rx.Component:
    """Sidebar que muestra el índice interactivo del Tema 1."""
    return rx.vstack(
        rx.heading("Tema 1: Números Naturales", size="5", color="white", margin_bottom="1.5em"),
        # --- NUEVO: BARRA DE PROGRESO DEL ALUMNO ---
        rx.vstack(
            rx.hstack(
                rx.text("Tu progreso del tema:", size="2", color="#94A3B8"),
                rx.text(f"{State.progreso}%", size="2", weight="bold", color="#818CF8"),
                width="100%",
                justify="between"
            ),
            rx.box(
                rx.progress(value=State.progreso, width="100%", color_scheme="indigo", border_radius="9999px"),
                width="100%",
                background="rgba(255, 255, 255, 0.04)",       # Fondo sutil del carril
                border="1px solid rgba(255, 255, 255, 0.12)",   # Borde blanco translúcido visible al 0%
                border_radius="9999px",                       # Formato de píldora redondeada
                padding="3px",                                  # Pequeño margen para que la barra "flote" dentro   
            ),
            margin_bottom="1.5em",
            width="100%"
            
        ),
        rx.vstack(
            rx.foreach(
                State.lessons_list,
                lambda lesson: rx.button(
                    lesson.title,  # Acceso por puntos oficial de dataclass
                    on_click=lambda: State.cargar_contenido_leccion(lesson.lesson_id),
                    width="100%",
                    color_scheme=rx.cond(State.selected_lesson == lesson.lesson_id, "indigo", "slate"),
                    variant=rx.cond(State.selected_lesson == lesson.lesson_id, "solid", "ghost"),
                   
                    # === TRUCO DE ORO: Evita el desborde de texto en los botones ===
                    
                    style = {
                        "height":"auto",  # Permite al botón crecer verticalmente si hay salto de línea
                        "justify-content": "start",
                        "white-space": "normal", # Permite que el texto salte de línea si es largo
                        "text-align": "left",  # Alineación de texto elegante para lectura
                        "padding_y": "1em",
                        "padding_x": "1em",
                        "cursor": "pointer",
                        "color": rx.cond(State.selected_lesson == lesson.lesson_id, "white", "#94A3B8"), # <-- Fuerza contraste
                    }
                ),
            ),
            width="100%",
            spacing="2",
        ),
        # =========================================================================
        # ESTILOS RESPONSIVOS PARA EL CONTENEDOR (Móvil vs Escritorio)
        # =========================================================================
        # [Móvil, Escritorio] -> 100% en móvil, 280px fijo en pantallas grandes
        width=["100%", "100%", "280px"],
        
        # Centra los elementos en móvil, los alinea a la izquierda en escritorio
        align_items=["center", "center", "stretch"], 
        
        height="auto" if ["100%", "100%", "100%"] else "100%", # Ajuste de altura responsiva
        padding="1.5em",
        background="rgba(30, 41, 59, 0.45)",
        backdrop_filter="blur(8px)",
        border="1px solid rgba(255, 255, 255, 0.08)",
        box_shadow="0 8px 32px 0 rgba(0, 0, 0, 0.37)",
        border_radius="16px",
        margin_bottom=["1.5em", "1.5em", "0"], # Añade separación abajo sólo en móviles
        )

# =========================================================================
# COMPONENTE 3: BURBUJAS DE CONVERSACIÓN DE CHAT
# =========================================================================

def mensaje_chat(interaccion: tuple[str, str]) -> rx.Component:
    """Muestra de forma impecable y separada el chat del alumno y del tutor."""
    return rx.vstack(
        # 1. BURBUJA DEL ALUMNO (A la derecha, morada, solo tu pregunta: interaccion)
        rx.box(
            rx.text(interaccion[0], color="white", weight="medium"),
            background_color="#6010DE",
            padding="0.8em 1.2em",
            border_radius="18px 18px 0px 18px",
            align_self="end",
            max_width="80%",
            box_shadow="0px 4px 15px rgba(96, 16, 222, 0.25)", # Sutil aura luminosa morada
        ),
        # 2. BURBUJA DEL TUTOR (A la izquierda, blanca, con formato Markdown: interaccion[1])
        # Solo se muestra si tiene contenido (evitando globos vacíos al inicio)
        rx.cond(
            interaccion[1] != "",
            rx.box(
                rx.markdown(
                    interaccion[1], 
                    color="#F1F5F9",
                    # =========================================================
                    #  LA SOLUCIÓN: Activamos el soporte matemático nativo
                    # =========================================================
                    math=True, 
                ),
               # === CAMBIO: Cristal esmerilado oscuro con borde fino ===
                background_color="rgba(30, 41, 59, 0.65)", 
                border="1px solid rgba(255, 255, 255, 0.08)",
                padding="0.8em 1.2em",
                border_radius="18px 18px 18px 0px",
                align_self="start",
                max_width="80%",
                box_shadow="0px 4px 20px rgba(0, 0, 0, 0.2)",
            ),
        ),
        width="100%",
        spacing="2",
    )


# =========================================================================
# COMPONENTE 4: CHAT 1 - TUTOR CONTEXTUAL DE LECCIÓN (GEMMA LOCAL)
# =========================================================================
def interfaz_tutor_leccion() -> rx.Component:
    """Cuadro de chat dinámico para la IA de Lección Contextual."""
    return rx.vstack(
        rx.heading("Tutor STEM Inteligente (Lección)", size="4", color="white"),
        rx.scroll_area(
            rx.vstack(
                rx.foreach(State.historial_leccion, mensaje_chat),
                width="100%",
                spacing="4",
            ),
            height="350px",
            width="100%",
            padding="1em",
            #  AÑADE ESTO (Línea translúcida ultra sutil):
            border="1px solid rgba(255, 255, 255, 0.04)",
            border_radius="12px",
            background="rgba(15, 23, 42, 0.2)", # Ligera base oscura para agrupar mensajes
        ),
        rx.hstack(
            rx.input(
                placeholder="Pregunta sobre esta lección...",
                value=State.pregunta_leccion,
                on_change=State.set_pregunta_leccion,
                width="100%",
            ),
            rx.button(
                rx.cond(State.cargando_leccion, rx.spinner(size="1"), "Preguntar"),
                on_click=State.preguntar_tutor_leccion,
                disabled=State.cargando_leccion,
            ),
            width="100%",
        ),
        width="100%",
        spacing="3",
        padding="1em",
    )

# =========================================================================
# COMPONENTE 5: CHAT 2 - ASISTENTE GLOBAL (DEEPSEEK)
# =========================================================================
def interfaz_tutor_ia() -> rx.Component:
    """Cuadro de chat dinámico con historial para consultas generales."""
    return rx.vstack(
        rx.heading("Tutor STEM Inteligente", size="4", color="black"),
        rx.scroll_area(
            rx.vstack(
                rx.foreach(State.historial_chat, mensaje_chat),
                width="100%",
                spacing="4",
            ),
            height="350px",
            width="100%",
            padding="1em",
            border=f"1px solid {rx.color('slate', 4)}",
            border_radius="10px",
        ),
        rx.hstack(
            rx.input(
                placeholder="Pregunta tu duda...",
                value=State.pregunta_tutor,
                on_change=State.set_pregunta_tutor,
                width="100%",
            ),
            rx.button(
                rx.cond(State.esta_cargando, rx.spinner(size="1"), "Enviar"),
                on_click=State.preguntar_tutor,
                disabled=State.esta_cargando,
            ),
            width="100%",
        ),
        width="100%",
        spacing="3",
        padding="1em",
    )

# =========================================================================
# COMPONENTE 6: TARJETAS DE MATERIAS
# =========================================================================
def card_materia(materia: Materia) -> rx.Component:
    """Tarjeta individual para el catálogo de la academia."""
    return rx.card(
        rx.vstack(
            rx.cond(
                materia.icono == "atom",
                rx.icon(tag="atom", size=30, color=rx.color(COLOR_PRIMARIO, 11)),
                rx.cond(
                    materia.icono == "bot",
                    rx.icon(tag="bot", size=30, color=rx.color(COLOR_PRIMARIO, 11)),
                    rx.cond(
                        materia.icono == "calculator",
                        rx.icon(tag="calculator", size=30, color=rx.color(COLOR_PRIMARIO, 11)),
                        rx.cond(
                            materia.icono == "magnet",
                            rx.icon(tag="magnet", size=30, color=rx.color(COLOR_PRIMARIO, 11)),
                            rx.cond(
                                materia.icono == "flask-conical",
                                rx.icon(tag="flask-conical", size=30, color=rx.color(COLOR_PRIMARIO, 11)),
                                rx.cond(
                                    materia.icono == "dna",
                                    rx.icon(tag="dna", size=30, color=rx.color(COLOR_PRIMARIO, 11)),
                                    rx.icon(tag="book-open", size=30, color=rx.color(COLOR_PRIMARIO, 11))
                                )
                            )
                        )
                    )
                )
            ),
            rx.heading(materia.nombre, size="4", color="black"),
            rx.badge(materia.curso, color_scheme="orange"),
            rx.text(materia.descripcion, size="2", color="gray"),
            rx.button(
                "Comprar " + materia.precio.to(str) + "€",
                style=estilo_boton_compra
            ),
            rx.button(
                rx.icon(tag="trash-2"),
                on_click=lambda: State.borrar_materia(materia.id),
                color_scheme="red",
                variant="soft",
                cursor="pointer"
            ),
            width="100%",
            justify="between",
            spacing="2",
            align="start"
        ),
        style=estilo_base_tarjeta
    )

# =========================================================================
# COMPONENTE 7: FORMULARIO REGISTRO MATERIAS
# =========================================================================
def formulario_materia() -> rx.Component:
    """Formulario interactivo para registrar materias."""
    return rx.vstack(
        rx.heading("Añadir Nueva Materia", size="5", color="white"),
        rx.input(
            placeholder="Nombre de la materia (ej: Álgebra)",
            on_change=State.set_nuevo_nombre,
            value=State.nuevo_nombre,
            width="100%"
        ),
        rx.select(
            ["1º ESO", "2º ESO", "3º ESO", "4º ESO", "1º Bachillerato", "2º Bachillerato"],
            on_change=State.set_nuevo_curso,
            width="100%"
        ),
        rx.text_area(
            placeholder="Descripción detallada...",
            on_change=State.set_nueva_descripcion,
            value=State.nueva_descripcion,
            width="100%"
        ),
        rx.input(
            placeholder="Precio en €",
            type="number",
            on_change=State.set_nuevo_precio,
            width="100%"
        ),
        rx.button(
            "Crear Materia",
            on_click=State.guardar_materia,
            color_scheme="green",
            width="100%",
            cursor="pointer"
        ),
        padding="2em",
        margin_top="15px",
        border=f"1px solid {rx.color('slate', 5)}",
        border_radius="15px",
        spacing="3",
        width="100%"
    )

# =========================================================================
# COMPONENTE 8: BUSCADOR DE MATERIAS
# =========================================================================
def buscador_materias() -> rx.Component:
    """Barra de búsqueda de materias moderna, elegante y de alto contraste."""
    return rx.hstack(
        rx.icon(tag="search", size=18, color="#E5E6ED"),
        rx.input(
            placeholder="Buscar materias por nombre o descripción...",
            value=State.buscar_texto,
            on_change=State.set_buscar_texto, # Reflex vincula el input con la variable de forma automática
            variant="surface",
            width="100%",
            color="black",
            focus_border_color="transparent",
        ),
        background="rgba(255, 255, 255, 0.08)",
        border="1px solid rgba(255, 255, 255, 0.2)",
        border_radius="10px",
        padding_x="1em",
        align_items="center",
        width="100%",
        margin_bottom="1.5em", # Separa estéticamente el buscador de la cuadrícula
    )


# =========================================================================
# COMPONENTE 9: PANTALLA DE ACCESO (LOGIN)
# =========================================================================
def login_admin() -> rx.Component:
    """Pantalla de acceso exclusivo centrada y a pantalla completa."""
    return rx.center(
        rx.form(
            rx.vstack(
                rx.heading("Panel de Control STEM", size="7", margin_bottom="1em", color="black"),
                rx.box(
                    rx.vstack(
                        rx.text("Introduce tus credenciales para gestionar los contenidos", size="2", opacity="0.8", color="slate"),
                        rx.input(
                            placeholder="Contraseña",
                            type="password",
                            name="password_field",
                            width="100%"
                        ),
                        rx.button(
                            "Acceder al Sistema",
                            type="submit",
                            color_scheme="indigo",
                            width="100%",
                            cursor="pointer"
                        ),
                        spacing="4"
                    ),
                    padding="2em",
                    border_radius="15px",
                    border=f"1px solid {rx.color('slate', 5)}",
                    background_color="white",
                    box_shadow="0px 10px 30px rgba(0,0,0,0.3)",
                    width="350px"
                ),
                align="center"
            ),
            on_submit=State.login
        ),
        width="100%",
        height="100vh",
        background=f"radial-gradient(circle at top, {rx.color('indigo', 3)}, {rx.color('slate', 2)})"
    )

def seccion_entrega_actividad() -> rx.Component:
    """Componente visual para que el alumno entregue su actividad y vea la corrección."""
    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.icon(tag="notebook-pen", size=22, color="#6010DE"),
                rx.heading("Ponte a prueba: Entrega tu solución", size="3", color="white"),
                spacing="2",
                align="center",
            ),
            rx.text(
                "Escribe aquí abajo tu respuesta paso a paso al ejercicio de la sección 'Actividad' de arriba. "
                "Tu tutor de IA lo evaluará al instante.",
                size="2",
                color="slate",
            ),
            rx.text_area(
                placeholder="Ej: El número 13 en el sistema egipcio se escribe con una herradura (que vale 10) y tres varas (que valen 1 cada una)...",
                value=State.respuesta_alumno,
                on_change=State.set_respuesta_alumno,
                width="100%",
                height="100px",
            ),
            rx.button(
                rx.cond(
                    State.cargando_correccion, 
                    rx.spinner(size="1"), 
                    "Enviar para corregir"
                ),
                on_click=State.corregir_actividad,
                disabled=State.cargando_correccion,
                color_scheme="indigo",
                width="100%",
                style={"cursor": "pointer"}
            ),
            
            # Mostrar la corrección inteligente del tutor de forma condicional si no está vacía
            rx.cond(
                State.correccion_tutor != "",
                rx.box(
                    rx.vstack(
                        rx.hstack(
                            rx.cond(
                                State.ultimo_resultado_correcto,
                                rx.icon(tag="circle-check", color="#38b000"),
                                rx.icon(tag="circle-alert", color="#ff9f1c")
                            ),
                            rx.heading(
                                rx.cond(State.ultimo_resultado_correcto, "¡Excelente resolución!", "Indicación del Tutor"),
                                size="2"
                            ),
                            spacing="2",
                            align="center"
                        ),
                        rx.text(State.correccion_tutor, size="2", color="white"),
                        spacing="2",
                        align="start",
                    ),
                    # Cambia de color dinámicamente si es correcto (verde oscuro) o hay que repasar (marrón cálido)
                    background_color=rx.cond(
                        State.ultimo_resultado_correcto,
                        "#132a13",  # Verde éxito
                        "#3d2612"   # Naranja/marrón repaso
                    ),
                    border=rx.cond(
                        State.ultimo_resultado_correcto,
                        "1px solid #38b000",
                        "1px solid #ff9f1c"
                    ),
                    border_radius="10px",
                    padding="1.2em",
                    width="100%",
                    margin_top="1em"
                )
            ),
            width="100%",
            spacing="3",
            align="start",
        ),
        width="100%",
        margin_top="2em",
        padding="1.5em",
        border="1px solid #1f2937",
        background_color="#111827",
    )


def seccion_test_hibrido() -> rx.Component:
    """Componente visual interactivo con grilla de opciones y feedback instantáneo."""
    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.icon(tag="circle-help", size=22, color="#6010DE"),
                rx.heading("Ponte a prueba: Pregunta de control", size="3", color="white"),
                spacing="2",
                align="center",
            ),
            rx.text(
                State.pregunta_test,
                size="2",
                weight="medium",
                color="slate",
                margin_bottom="0.5em",
            ),
            
            # Muestra los botones de opciones generados de forma dinámica
            rx.vstack(
                rx.foreach(
                    State.opciones_test,
                    lambda opcion: rx.button(
                        opcion,
                        width="100%",
                        # El botón cambia a color índigo si el alumno hace clic sobre él
                        color_scheme=rx.cond(State.opcion_seleccionada == opcion, "indigo", "slate"),
                        variant=rx.cond(State.opcion_seleccionada == opcion, "solid", "outline"),
                        on_click=lambda: State.seleccionar_opcion(opcion),
                        style={
                            "justify-content": "start",
                            "cursor": "pointer",
                            "white-space": "normal",
                            "text-align": "left",
                            "padding_y": "1.2em"
                        }
                    )
                ),
                width="100%",
                spacing="2",
            ),
            
            # Botón de enviar para comprobar la respuesta
            rx.button(
                rx.cond(
                    State.cargando_leccion,
                    rx.spinner(size="1"),
                    "Comprobar respuesta"
                ),
                on_click=State.verificar_respuesta_test,
                disabled=State.cargando_leccion,
                color_scheme="green",
                width="100%",
                margin_top="1em",
                style={"cursor": "pointer"}
            ),
            
            # Cuadro condicional de feedback rápido (Verde si acierta, Marrón si requiere pista)
            rx.cond(
                State.mostrar_feedback_test,
                rx.box(
                    rx.vstack(
                        rx.hstack(
                            rx.cond(
                                State.test_correcto,
                                rx.icon(tag="circle-check", color="#38b000"),
                                rx.icon(tag="lightbulb", color="#ff9f1c")
                            ),
                            rx.heading(
                                rx.cond(State.test_correcto, "¡Respuesta Correcta!", "Sugerencia del Tutor"),
                                size="2"
                            ),
                            spacing="2",
                            align="center"
                        ),
                        rx.text(State.feedback_test, size="2", color="white"),
                        spacing="2",
                        align="start",
                    ),
                    background_color=rx.cond(
                        State.test_correcto,
                        "#132a13",  # Verde éxito
                        "#3d2612"   # Marrón cálido para pista
                    ),
                    border=rx.cond(
                        State.test_correcto,
                        "1px solid #38b000",
                        "1px solid #ff9f1c"
                    ),
                    border_radius="10px",
                    padding="1.2em",
                    width="100%",
                    margin_top="1em"
                )
            ),
            width="100%",
            spacing="3",
            align="start",
        ),
        width="100%",
        margin_top="2em",
        padding="1.5em",
        border="1px solid #1f2937",
        background_color="#111827",
    )

