import reflex as rx
from .components import navbar, card_materia, formulario_materia, interfaz_tutor_ia, login_admin
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
                
                spacing="3",
                width="100%", # Se estrecha en PC para no verse tan largo
                align_items="center",
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
                # Lado izquierdo PROTEGIDO
                rx.box(
                    rx.cond(
                        State.esta_autenticado,
                        # SI ESTÁ LOGUEADO: Muestra gestión
                        rx.vstack(
                            formulario_materia(),
                            rx.button(
                                "Cerrar Sesión", 
                                on_click=State.logout, 
                                variant="ghost", 
                                color_scheme="red",
                                margin_top="1em"
                            ),
                            width="100%"
                        ),
                        # SI NO ESTÁ LOGUEADO: Muestra login
                        login_admin()
                    ),
                    width="30%"
                ),
                
                # Lado derecho: Las tarjetas (Visibles para todos)
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

            rx.divider(margin_y="3em"), # Separador visual profesional

            rx.vstack(
                rx.heading("Asistencia Inteligente STEM 24/7", size="7", align="center", color="white"),
                rx.text("Pregunta cualquier duda sobre tus cursos y el tutor IA te responderá al instante.", align="center", opacity="0.8",color="white"),
                
                # LLAMADA ÚNICA AL NUEVO COMPONENTE
                # Este componente contiene internamente el historial, el input y el botón
                rx.box(
                    interfaz_tutor_ia(), 
                    width="100%",
                    max_width="900px", # Ancho ideal para lectura
                    margin_top="1.5em",
                ),
                width="100%",
                spacing="4",
                padding_y="2em",
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