import reflex as rx
from .components import navbar, card_materia, formulario_materia, interfaz_tutor_ia, login_admin
from .state import State
from .styles import (
    COLOR_BLANCO_PURO, 
    COLOR_PRIMARIO, 
    ESTILO_BOTON_FILTRO_BASE, 
    COLOR_FONDO, 
    COLOR_SECUNDARIO
)

def index() -> rx.Component:
    return rx.cond(
        State.esta_autenticado,
        # --- VISTA 1: MODO ADMINISTRADOR (Academia Completa) ---
        rx.vstack(
            navbar(),
            rx.container(
                # 1. TÍTULO DINÁMICO
                rx.heading(
                    "Apoyo Escolar para ", State.filtro_curso, 
                    size={"initial": "6", "sm": "8", "md": "9"},
                    align="center",
                    width="100%",
                    margin_y="0.5em",
                    background_image="linear-gradient(to right, #EEF750, #FF9000)",
                    background_clip="text",
                    color="transparent",
                ),

                # 2. BUSCADOR REINTEGRADO (Lo que faltaba)
                rx.vstack(
                    rx.input(
                        placeholder="¿Qué quieres aprender hoy? (ej: Física, Cálculo...)",
                        on_change=State.set_buscar, # Búsqueda reactiva vinculada al State [1]
                        width="100%",
                        size="3",
                        margin_y="1em",
                    ),
                    spacing="3",
                    width="100%",
                    align_items="center",
                ),

                # 3. FILTROS POR CURSO
                rx.flex(
                    rx.foreach(
                        ["Todos", "1º ESO", "2º ESO", "3º ESO", "4º ESO", "1º Bachillerato", "2º Bachillerato"],
                        lambda curso: rx.button(
                            curso,
                            on_click=lambda: State.set_filtro(curso),
                            color=COLOR_BLANCO_PURO, 
                            # Esto estaba bien (3 argumentos)
                            color_scheme=rx.cond(State.filtro_curso == curso, COLOR_SECUNDARIO, "black"),
                            # AQUÍ ESTABA EL ERROR (He quitado el argumento repetido)
                            variant=rx.cond(State.filtro_curso == curso, "solid", "outline"),
                            style=ESTILO_BOTON_FILTRO_BASE,
                        )
                    ),
                    spacing="3",
                    margin_y="1.5em",
                    flex_wrap="wrap",
                    justify="center",
                ),

                # 4. GESTIÓN + GRID DE MATERIAS
                rx.hstack(
                    rx.box(
                        rx.vstack(
                            formulario_materia(),
                            rx.button(
                                "Cerrar Sesión", 
                                on_click=State.logout, 
                                # Aplicamos el mismo degradado que el título
                                background="linear-gradient(to right, #FF8C00, #ED1C24)",
                                color="white", # Forzamos el texto a blanco para que resalte
                                width="100%",
                                margin_top="1em",
                                # Añadimos un pequeño efecto al pasar el ratón para que sea profesional
                                _hover={
                                    "opacity": "0.8",
                                    "transform": "scale(1.02)",
                                    "transition": "all 0.2s ease-in-out",
                                },
                                cursor="pointer",
                            ),   
                            width="100%"
                        ),
                        width="30%"
                    ),
                    rx.box(
                        rx.grid(
                            rx.foreach(State.materias_filtradas, card_materia),
                            columns={"initial": "1", "sm": "1", "md": "2"}, 
                            spacing="4",
                        ),
                        width="70%"
                    ),
                    width="100%",
                    spacing="5",
                    align_items="start",
                ),

                rx.divider(margin_y="3em"),

                # 5. ASISTENCIA IA
                rx.vstack(
                    rx.heading("Asistencia Inteligente STEM 24/7", size="7", align="center", color="white"),
                    rx.text("Pregunta cualquier duda y el tutor IA te responderá al instante.", align="center", opacity="0.8", color="white"),
                    rx.box(
                        interfaz_tutor_ia(), 
                        width="100%",
                        max_width="900px",
                        margin_top="1.5em",
                    ),
                    width="100%",
                    spacing="4",
                    padding_y="2em",
                ),

                size="3",
                padding_x=["1em", "2em", "4em"],
            ),
            background=f"radial-gradient(circle at center, {COLOR_FONDO} 0%, #000000 100%)",
            min_height="100vh",
            width="100%",
            align_items="center",
        ),
        
        # --- VISTA 2: PANTALLA DE INICIO (Solo Login) ---
        login_admin()
    )

app = rx.App()
app.add_page(index, on_load=State.cargar_materias)

