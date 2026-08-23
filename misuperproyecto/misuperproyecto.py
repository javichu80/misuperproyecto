import reflex as rx
from .components import (
    navbar, 
    card_materia, 
    formulario_materia, 
    interfaz_tutor_ia,      # IA Genérica (DeepSeek - Al final)
    interfaz_tutor_leccion, # IA Contextual (Gemma - Arriba)
    login_admin, 
    sidebar_lecciones
)
from .state import State

COLOR_FONDO = "#738CC9"

def index() -> rx.Component:
    return rx.cond(
        State.esta_autenticado,
        # --- VISTA 1: MODO ADMINISTRADOR (Academia Completa) ---
        rx.vstack(
            navbar(),
            
            # SECCIÓN SUPERIOR: "VISTA DE ESTUDIO" (Novedad del Blueprint)
            rx.container(
                rx.heading(
                    "Apoyo Escolar para " + State.filtro_curso, 
                    size="8",
                    align="center",
                    width="100%",
                    margin_y="0.5em",
                    background_image="linear-gradient(to right, #FF8C00, #ED1C24)",
                    background_clip="text",
                    color="transparent",
                ),

                # Contenedor Flexible Horizontal de Estudio
                rx.flex(
                    # 1. Sidebar (Menú de lecciones) - 25% de ancho
                    rx.box(
                        sidebar_lecciones(),
                        width=["100%", "100%", "25%"],
                        margin_bottom=["1.5em", "1.5em", "0em"],
                    ),
                    
                    # 2. Visor de Teoría Markdown - 50% de ancho
                    rx.box(
                        rx.scroll_area(
                            rx.markdown(
                                State.lesson_content,
                                color="black",
                            ),
                            height="60vh",
                            scrollbars="vertical",
                        ),
                        padding="1.5em",
                        background=rx.color("slate", 2),
                        border_radius="15px",
                        border=f"1px solid {rx.color('slate', 4)}",
                        width=["100%", "100%", "50%"],
                        margin_x=["0em", "0em", "1em"],
                    ),

                    # 3. Tutor IA Contextual de Lección (Gemma) - 25% de ancho
                    rx.box(
                        interfaz_tutor_leccion(),
                        width=["100%", "100%", "25%"],
                    ),
                    
                    width="100%",
                    flex_wrap="wrap",
                    align_items="stretch",
                ),
                
                size="3",
                padding_x=["1em", "2em", "4em"],
                margin_bottom="3em",
            ),

            rx.divider(color_scheme="gray"),

            # SECCIÓN INFERIOR: GESTIÓN DE MATERIAS Y CHAT GENÉRICO
            rx.container(
                rx.heading("Gestión de Materias STEM", size="6", color="white", margin_y="1em"),
                rx.hstack(
                    rx.box(
                        rx.vstack(
                            formulario_materia(),
                            rx.button(
                                "Cerrar Sesión", 
                                on_click=State.logout, 
                                background="linear-gradient(to right, #FF8C00, #ED1C24)",
                                color="black",
                                width="100%",
                                margin_top="1em",
                                cursor="pointer",
                            ),
                            width="100%"
                        ),
                        width="30%"
                    ),
                    # Columna Derecha (Buscador, Filtros Rápidos y Cuadrícula) - 70% ancho
                    rx.box(
                        rx.vstack(
                            # --- BARRA DE FILTRADO Y BÚSQUEDA COMPLETA (¡RECUPERADA!) ---
                            rx.hstack(
                                rx.input(
                                    placeholder="Buscar materia por nombre o descripción...",
                                    value=State.buscar_texto,
                                    on_change=State.set_buscar_texto,
                                    width="100%",
                                    background_color="rgba(255, 255, 255, 0.05)",
                                    border=f"1px solid {rx.color('slate', 5)}",
                                    color="white",
                                ),
                                rx.button(
                                    rx.icon(tag="search", size=18),
                                    color_scheme="indigo",
                                    variant="solid",
                                ),
                                width="100%",
                                spacing="3",
                                margin_bottom="1em",
                            ),
                            
                            # Botones de filtro rápido para encender/apagar cursos de tarjetas
                            rx.hstack(
                                rx.button(
                                    "Todas",
                                    on_click=lambda: State.set_filtro_curso("Todos"),
                                    color_scheme=rx.cond(State.filtro_curso == "Todos", "indigo", "slate"),
                                    variant=rx.cond(State.filtro_curso == "Todos", "solid", "ghost"),
                                    size="2",
                                    cursor="pointer",
                                ),
                                rx.button(
                                    "1º ESO",
                                    on_click=lambda: State.set_filtro_curso("1º ESO"),
                                    color_scheme=rx.cond(State.filtro_curso == "1º ESO", "indigo", "slate"),
                                    variant=rx.cond(State.filtro_curso == "1º ESO", "solid", "ghost"),
                                    size="2",
                                    cursor="pointer",
                                ),
                                rx.button(
                                    "2º ESO",
                                    on_click=lambda: State.set_filtro_curso("2º ESO"),
                                    color_scheme=rx.cond(State.filtro_curso == "2º ESO", "indigo", "slate"),
                                    variant=rx.cond(State.filtro_curso == "2º ESO", "solid", "ghost"),
                                    size="2",
                                    cursor="pointer",
                                ),
                                rx.button(
                                    "3º ESO",
                                    on_click=lambda: State.set_filtro_curso("3º ESO"),
                                    color_scheme=rx.cond(State.filtro_curso == "3º ESO", "indigo", "slate"),
                                    variant=rx.cond(State.filtro_curso == "3º ESO", "solid", "ghost"),
                                    size="2",
                                    cursor="pointer",
                                ),
                                rx.button(
                                    "4º ESO",
                                    on_click=lambda: State.set_filtro_curso("4º ESO"),
                                    color_scheme=rx.cond(State.filtro_curso == "4º ESO", "indigo", "slate"),
                                    variant=rx.cond(State.filtro_curso == "4º ESO", "solid", "ghost"),
                                    size="2",
                                    cursor="pointer",
                                ),
                                spacing="2",
                                margin_bottom="1.5em",
                            ),
                            
                            # Cuadrícula con las tarjetas de materias filtradas reactivamente
                            rx.grid(
                                rx.foreach(State.materias_filtradas, card_materia),
                                columns={"initial": "1", "sm": "1", "md": "2"}, 
                                spacing="4",
                                width="100%",
                            ),
                            width="100%",
                            align_items="start",
                        ),
                        width="70%"
                    ),
                    width="100%",
                    spacing="5",
                    align_items="start",
                ),
                
                rx.divider(color_scheme="gray", margin_y="2em"),
                
                # CHAT GENÉRICO GLOBAL (DeepSeek - Al final de la página)
                rx.vstack(
                    rx.heading("Asistente STEM de Consulta General", size="5", color="white", margin_bottom="0.5em"),
                    rx.box(
                        interfaz_tutor_ia(),
                        background=rx.color("slate", 2),
                        border_radius="15px",
                        padding="1em",
                        width="100%",
                    ),
                    width="100%",
                ),
                
                size="3",
                padding_x=["1em", "2em", "4em"],
                padding_y="2em",
            ),
            
            background=f"radial-gradient(circle at center, {COLOR_FONDO} 0%, #000000 100%)",
            min_height="100vh",
            width="100%",
        ),
        
        # --- VISTA 2: PANTALLA DE INICIO (Solo Login) ---
        login_admin()
    )

app = rx.App()
app.add_page(index, on_load=State.iniciar_pagina)