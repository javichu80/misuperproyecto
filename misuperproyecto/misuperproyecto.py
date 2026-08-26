import reflex as rx
from .components import (
    navbar, 
    buscador_materias,
    card_materia, 
    formulario_materia, 
    interfaz_tutor_ia,      # IA Genérica (DeepSeek - Al final)
    interfaz_tutor_leccion, # IA Contextual (Gemma - Arriba)
    login_admin, 
    sidebar_lecciones,
    seccion_entrega_actividad,
    seccion_test_hibrido
)
from .state import State

COLOR_FONDO = "#4E6AC0"  # Unificamos con el tono oscuro profundo "Dark STEM" de tu paleta

def index() -> rx.Component:
    return rx.cond(
        State.esta_autenticado,
        # --- VISTA 1: MODO ALUMNO/ADMINISTRADOR AUTENTICADO ---
        rx.vstack(
            navbar(),
            
            # ==========================================
            # SECCIÓN SUPERIOR: "VISTA DE ESTUDIO" (Sprint 4)
            # ==========================================
            rx.box(
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

                # Contenedor Flexible Horizontal de Estudio (100% Adaptativo)
                rx.flex(
                    # 1. Sidebar (Menú de lecciones) - 25% de ancho en PC, 100% en móvil
                    rx.box(
                        sidebar_lecciones(),
                        width=["100%", "100%", "18%"],
                        margin_bottom=["1.5em", "0.5em", "0em"],
                    ),
                    
                    # 2. Visor de Teoría Markdown - 48% de ancho en PC (para dar aire), 100% en móvil
                    rx.box(
                        rx.scroll_area(
                            rx.vstack( # <-- Añadimos un vstack para apilar el texto y el formulario
                                rx.markdown(
                                    State.lesson_content,
                                    color="black",
                                ),
                                seccion_test_hibrido(), # <-- ¡Aquí insertamos el formulario de entrega!
                                width="100%",
                                spacing="4",
                            ),
                            height="72vh",
                            scrollbars="vertical",
                        ),
                        padding="1.5em",
                        background=rx.color("slate", 2),
                        border_radius="15px",
                        border=f"1px solid {rx.color('slate', 4)}",
                        width=["100%", "100%", "56%"],
                        margin_x=["0em", "0em", "1%"],
                        margin_bottom=["1.5em", "1.5em", "0em"],
                    ),

                    # 3. Tutor IA Contextual de Lección (Gemma) - 25% de ancho en PC, 100% en móvil
                    rx.box(
                        interfaz_tutor_leccion(),
                        width=["100%", "100%", "24%"],
                    ),
                    
                    width="100%",
                    flex_direction=["column", "column", "row"],  # En columna en móvil/tablet, fila en PC
                    justify_content="between",
                    align_items="stretch",
                    spacing="4",
                ),
                
                # ESTILOS DE ANCHO TOTAL FLUIDO:
                width="100%",
                max_width="1600px", 
                margin_x="auto",                # Centra la sección horizontalmente en la pantalla
                padding_x=["1em", "2em", "4em"],
                margin_bottom="3em",
            ),

            rx.divider(color_scheme="gray"),

            # ==========================================
            # SECCIÓN INFERIOR: GESTIÓN DE MATERIAS Y CHAT GENÉRICO
            # ==========================================
            rx.box(
                rx.heading("Gestión de Materias STEM", size="6", color="white", margin_y="1em"),
                buscador_materias(),
                # Contenedor Flexible Inferior (100% Adaptativo)
                rx.grid(
                    # Columna Izquierda: Formulario de Materia y Cerrar Sesión (30% ancho en PC, 100% en móvil)
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
                            width="100%",
                            
                        ),
                        width="100%",
                         # ¡CORREGIDO! Usamos diccionarios para breakpoints en propiedades de grid
                        grid_column={"initial": "span 1", "md": "1 / 2"},  
                    ),
                    
                    # Columna Central: Cuadrícula Elástica de Materias (38% ancho en PC, 100% en móvil)
                    rx.box(
                        rx.vstack(
                            rx.heading("Materias Disponibles", size="4", color="white", margin_bottom="0.5em"),
                            rx.grid(
                                rx.foreach(
                                    State.materias_filtradas,  # Recorre tu lista de materias cargada en State
                                    card_materia
                                ),
                                columns={"initial": "1", "sm": "1", "md": "2"},  # 1 columna en móvil/tablet, 2 columnas en PC
                                spacing="4",
                                width="100%",
                            ),
                           # width="100%",
                        ),
                        width="100%",
                        grid_column={"initial": "span 1", "md": "2 / 3"},  # Segundo track
                        margin_bottom=["2em", "2em", "0em"],
                    ),

                    # Columna Derecha: Chat Global Genérico (DeepSeek) (30% ancho en PC, 100% en móvil)
                    rx.box(
                        interfaz_tutor_ia(),
                        width="100%",
                        grid_column={"initial": "span 1", "md": "3 / 4"},  # Tercer track
                    ),
                    
                    # ¡CLAVE DE LA REJILLA RESPONSIVA!
                    columns={"initial": "1", "md": "3"},  # 1 columna en móvil/tablet, 3 en PC
                    grid_template_columns={"initial": "1fr", "md": "30% 38% 30%"},  # Reparto exacto de proporciones en PC
                    width="100%",
                    spacing="4",
                ),
                
                # ESTILOS DE ANCHO TOTAL FLUIDO:
                width="100%",
                max_width="1600px",
                margin_x="auto",                # Centra la sección horizontalmente en la pantalla
                padding_x=["1em", "2em", "4em"],
                margin_bottom="3em",
            ),
            
            background_color=COLOR_FONDO,
            min_height="100vh",
            width="100%",
            spacing="0",
        ),
        # --- VISTA 2: LOGIN ---
        login_admin()
        )
    

# Configuración e inicialización de tu aplicación Reflex
app = rx.App()
app.add_page(index, on_load=State.iniciar_pagina)














