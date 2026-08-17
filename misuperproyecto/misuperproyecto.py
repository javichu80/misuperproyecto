import reflex as rx
from .components import navbar, card_materia, formulario_materia
from .state import State
from .styles import COLOR_BLANCO_PURO, COLOR_PRIMARIO, ESTILO_BOTON_FILTRO_BASE, COLOR_FONDO, COLOR_SECUNDARIO

def index() -> rx.Component:
    return rx.vstack(
        navbar(),
        rx.container(
            # Título dinámico compatible con Reflex
            rx.heading("Apoyo Escolar para ", State.filtro_curso, 
                        size={"initial": "6", "sm": "8", "md": "9"}, # Más pequeño en móvil, gigante en PC
                        align="center",
                        width="100%",
                        margin_y="0.5em",
                        # EFECTO DE GRADIENTE EN TEXTO:
                        background_image="linear-gradient(to right, #EEF750, #FF9000)",
                        background_clip="text",
                        color="transparent", # Necesario para que se vea el fondo de imagen (gradiente)
            ),

            rx.vstack(
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
                    size="3"
                ),
                rx.button(
                    "Preguntar", 
                    on_click=State.preguntar_tutor, # Llama a la lógica de la IA
                    loading=State.esta_cargando,   # Muestra el spinner visual
                    width=["100%", "auto"], # Ocupa todo en móvil, tamaño normal en PC
                    size="3",
                    color_scheme=COLOR_PRIMARIO,
                    margin_y="1em",
                ),
                spacing="3",
                width="100%", # Se estrecha en PC para no verse tan largo
                align_items="center",
            ),
            rx.box(
                rx.cond(
                    State.respuesta_tutor != "", # Solo se muestra si hay respuesta
                    rx.vstack(
                        rx.text("🤖 Respuesta del Tutor:", weight="bold", color_scheme=COLOR_PRIMARIO),
                        rx.markdown(State.respuesta_tutor),
                        background=rx.color("slate", 3),
                        padding="1.5em",
                        border_radius="10px",
                        width="100%",
                        max_height="300px",  # Altura máxima antes de mostrar scroll [3]
                        overflow_y="auto",   # Muestra la barra de desplazamiento solo si es necesario [1, 2]
                        margin_top="1em",
                        align_items="start", # Alinea el texto a la izquierda
                    )
                ),
                width="100%" # Mismo ancho que los inputs para coherencia
            ),
            rx.flex(
                # Botones inteligentes: cambian de color según el estado
                rx.foreach(
                    ["Todos", "1º ESO", "2º ESO", "3º ESO", "4º ESO", "1º Bachillerato", "2º Bachillerato"],
                    lambda curso: rx.button(
                        curso,
                        on_click=lambda: State.set_filtro(curso),
                        # Forzamos el color del texto a blanco puro
                        color=COLOR_BLANCO_PURO, 
                        # Lógica condicional nativa para resaltar el curso activo [Conversación previa]
                        color_scheme=rx.cond(State.filtro_curso == curso, COLOR_SECUNDARIO, "black"),
                        variant=rx.cond(State.filtro_curso == curso, "solid", "outline"),
                        style=ESTILO_BOTON_FILTRO_BASE,
                    )
                ),
                
                spacing="3",
                margin_y="1.5em",
                flex_wrap="wrap", # <--- CLAVE: Si no caben, saltan de línea automáticamente
                justify="center", # Centra los botones en cualquier pantalla
            ),


            rx.hstack(
                # Lado izquierdo: El formulario
                rx.box(formulario_materia(), width="30%"),
                # Lado derecho: Las tarjetas existentes
                rx.box(
                    rx.grid(
                        rx.foreach(State.materias_filtradas, card_materia),
                        flex_wrap="wrap",
                        spacing="4",
                    ),
                    width="70%"
                ),
                width="100%",
                spacing="5",
            ),

            # Hacemos que el contenedor no sea rígido
            size="3", # Tamaño intermedio de Reflex para centrar el contenido
            padding_x=["1em", "2em", "4em"], # Margen lateral que crece con la pantalla
        ),
        background=f"radial-gradient(circle at center, {COLOR_FONDO} 0%, #000000 100%)",
        min_height="100vh", # Asegura que el fondo cubra toda la pantalla
        width="100",
        align_items="center",
            
    )
app = rx.App()
app.add_page(index, on_load=State.cargar_materias)# <-- Llama a la función al cargar