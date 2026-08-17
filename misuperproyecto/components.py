import reflex as rx
from rxconfig import config
from .state import State
from .models import Materia
from .styles import estilo_base_tarjeta, estilo_boton_compra, COLOR_PRIMARIO, COLOR_BRANDNAME

# Asegúrate de que esta función esté presente
def navbar() -> rx.Component:
    return rx.hstack(
        rx.heading(State.brand_name, size="7", color=COLOR_BRANDNAME),
        rx.spacer(),
        rx.link("Inicio", href="/", color="white"),
        rx.link("Productos", href="/productos", color="green"),
        # ... resto de estilos del navbar
    )

# --- 2. COMPONENTES DEL TUTOR IA (EDUCACIÓN 3.0) ---
def mensaje_chat(interaccion: tuple[str, str]) -> rx.Component:
    """Corrige el error de la imagenIA separando pregunta y respuesta."""
    return rx.vstack(
        # 1. BURBUJA DEL ALUMNO (Índice 0: lo que tú escribes)
        rx.box(
            # Usamos interaccion para sacar solo tu pregunta
            rx.text(interaccion[0], color="white", weight="medium"),
            background_color="#6010DE", 
            padding="0.8em 1.2em",
            border_radius="18px 18px 0px 18px",
            align_self="end", # Se pega a la derecha
            max_width="80%",
        ),
        
        # 2. BURBUJA DEL TUTOR IA (Índice 1: lo que responde la IA)
        rx.box(
            # IMPORTANTE: rx.markdown interpreta las negritas y fórmulas de la imagen
            rx.markdown(
                interaccion[1],
                # ESTA LÍNEA ES LA CLAVE PARA LAS FÓRMULAS:
                extensions=["latex"], 
                component_props={
                    "p": {"margin_bottom": "1em", "line_height": "1.6"},
                    "ul": {"padding_left": "1.5em"},
                }
            ),
            background_color="#F3F4F6", # Gris claro para diferenciar
            padding="1em 1.5em",
            border_radius="18px 18px 18px 0px",
            align_self="start", # Se pega a la izquierda
            max_width="90%",
            color="slate",
            border="1px solid #E5E7EB",
        ),
        spacing="3", # Crea el espacio vertical que falta en tu imagen
        width="100%",
        margin_y="1em",
    )

def interfaz_tutor_ia() -> rx.Component:
    """Cuadro de chat dinámico con historial."""
    return rx.vstack(
        rx.heading("Tutor STEM Inteligente", size="4", color="white"),
        rx.scroll_area(
            rx.vstack(
                rx.foreach(State.historial_chat, mensaje_chat),
                width="100%",
                spacing="4",
            ),
            height="350px",
            width="100%",
            padding="1em",
            border="1px solid #E5E7EB",
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
                on_click=State.preguntar_tutor, # Llamada al backend asíncrono
                disabled=State.esta_cargando,
            ),
            width="100%",
        ),
        width="100%",
        spacing="3",
        padding="1em",
    )

def card_materia(materia: Materia) -> rx.Component: # Cambiado de dict a Materia
    return rx.card(
        rx.vstack(
            # Cadena de condiciones anidada correctamente
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
                                    # Icono por defecto si nada coincide
                                    rx.icon(tag="book-open", size=30, color=rx.color(COLOR_PRIMARIO, 11))
                                )
                            )
                        )
                    )
                )
            ),
            # Acceso profesional por puntos
            rx.heading(materia.nombre, size="4"),
            rx.badge(materia.curso, color_scheme="orange"),
            rx.text(materia.descripcion, size="2"),
            rx.button(
                "Comprar ", materia.precio, "€", 
                style=estilo_boton_compra
            ),
            # BOTÓN DE ELIMINAR (Nuevo)
            rx.button(
                rx.icon(tag="trash-2"), # Icono de papelera
                on_click=lambda: State.borrar_materia(materia.id),
                color_scheme="red",
                variant="soft",
            ),
            width="100%",
            justify="between",
            spacing="1",
            align="start",
        ),
        style=estilo_base_tarjeta
    )


def formulario_materia() -> rx.Component:
    return rx.vstack(
        rx.heading("Añadir Nueva Materia", size="5", color="white"),
        rx.input(
            placeholder="Nombre de la materia (ej: Álgebra)",
            on_change=State.set_nuevo_nombre,
            value=State.nuevo_nombre,
            width="100%",
        ),
        rx.select(
            ["1º ESO", "2º ESO", "3º ESO", "4º ESO", "1º Bachillerato", "2º Bachillerato"],
            on_change=State.set_nuevo_curso,
            width="100%",
        ),
        rx.text_area(
            placeholder="Descripción detallada...",
            on_change=State.set_nueva_descripcion,
            value=State.nueva_descripcion,
            width="100%",
        ),
        rx.input(
            placeholder="Precio en €",
            type="number",
            on_change=State.set_nuevo_precio,
            width="100%",
        ),
        rx.button(
            "Crear Materia",
            on_click=State.guardar_materia,
            color_scheme="green",
            width="100%",
        ),
        padding="2em",
        margin_top= "15px",
        border=f"1px solid {rx.color('slate', 5)}",
        border_radius="15px",
        spacing="3",
        width="100%",
    )

def login_admin() -> rx.Component:
    """Pequeño formulario para autenticarse."""
    return rx.vstack(
        rx.heading("Acceso Administrador", size="4", color="white"),
        rx.input(
            placeholder="Contraseña",
            type="password",
            on_change=State.set_password_input,
            value=State.password_input,
            width="100%",
        ),
        rx.button(
            "Entrar",
            on_click=State.login,
            color_scheme="indigo",
            width="100%",
        ),
        padding="1.5em",
        border=f"1px solid {rx.color('slate', 5)}",
        border_radius="10px",
        spacing="3",
    )