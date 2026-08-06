import reflex as rx
from .components import navbar, card_materia
from .state import State
from .styles import COLOR_PRIMARIO, ESTILO_BOTON_FILTRO_BASE

def index() -> rx.Component:
    return rx.vstack(
        navbar(),
        rx.container(
            # Título dinámico compatible con Reflex
            rx.heading("Apoyo Escolar para ", State.filtro_curso, margin_y="1em"),
            rx.input(
                placeholder="¿Qué quieres aprender hoy? (ej: Física, Cálculo...)",
                on_change=State.set_buscar, # Búsqueda reactiva mientras escribes
                width="100%",
                size="3",
                margin_y="1em",
            ),
            rx.input(
                placeholder="Escribe tu duda aquí...",
                on_change=State.set_pregunta_tutor, # Enchufado al setter
                width="100%",
            ),
            rx.button(
                "Preguntar", 
                on_click=State.preguntar_tutor, # Llama a la lógica de la IA
                loading=State.esta_cargando,   # Muestra el spinner visual
            ),
            rx.box(
                rx.cond(
                    State.respuesta_tutor != "", # Solo se muestra si hay respuesta
                    rx.vstack(
                        rx.text("🤖 Respuesta del Tutor:", weight="bold", color_scheme=COLOR_PRIMARIO),
                        rx.text(State.respuesta_tutor),
                        background=rx.color("slate", 3),
                        padding="1.5em",
                        border_radius="10px",
                        width="100%",
                        margin_top="1em",
                    )
                ),
                width="100%",
            ),
            rx.hstack(
                # Botones inteligentes: cambian de color según el estado
                rx.foreach(
                    ["Todos", "1º ESO", "2º ESO", "3º ESO", "4º ESO", "1º Bachillerato", "2º Bachillerato"],
                    lambda curso: rx.button(
                        curso,
                        on_click=lambda: State.set_filtro(curso),
                        # Lógica condicional nativa para resaltar el curso activo [Conversación previa]
                        color_scheme=rx.cond(State.filtro_curso == curso, COLOR_PRIMARIO, "gray"),
                        variant=rx.cond(State.filtro_curso == curso, "solid", "outline"),
                        style=ESTILO_BOTON_FILTRO_BASE,
                    )
                ),
                
                spacing="4", margin_y="1em",
            ),
            rx.flex(
                rx.foreach(State.paquetes_filtrados, card_materia),
                wrap="wrap", spacing="4",
            ),
            padding="2em",
        )
    )

app = rx.App()
app.add_page(index)