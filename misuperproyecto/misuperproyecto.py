import reflex as rx
from .components import navbar
from .state import State

def card_materia(materia: dict) -> rx.Component:
    return rx.card(
        rx.vstack(
            # SOLUCIÓN: Usamos rx.cond para elegir el icono con un texto fijo
            rx.cond(
                materia["icono"] == "atom",
                rx.icon(tag="atom", size=30, color=rx.color("iris", 11)),
                rx.cond(
                    materia["icono"] == "bot",
                    rx.icon(tag="bot", size=30, color=rx.color("iris", 11)),
                        rx.cond(
                            materia["icono"] == "calculator",
                            rx.icon(tag="calculator", size=30, color=rx.color("iris", 11)),
                                rx.cond(
                                    materia["icono"] == "magnet",
                                    rx.icon(tag="magnet", size=30, color=rx.color("iris", 11)),
                                        rx.cond(
                                            materia["icono"] == "cpu",
                                            rx.icon(tag="cpu", size=30, color=rx.color("iris", 11)),
                                                rx.cond(
                                                    materia["icono"] == "settings",
                                                    rx.icon(tag="settings", size=30, color=rx.color("iris", 11)),
                                                        rx.cond(
                                                            materia["icono"] == "flask-conical", # <--- ¿Coincide este texto con state.py?
                                                            rx.icon(tag="flask-conical", size=30, color=rx.color("iris", 11)),
                                                                rx.cond(
                                                                    materia["icono"] == "grid", # <--- ¿Coincide este texto con state.py?
                                                                    rx.icon(tag="grid", size=30, color=rx.color("iris", 11)),
                                                                    # ICONO POR DEFECTO: Siempre debe haber un cierre
                                                                    rx.icon(tag="book-open", size=30, color=rx.color("iris", 11))
                                                                )       
                                                        )
                                                )
                                        )
                                )
                        )
                    )
            ),
            # Acceso profesional por clave de diccionario
            rx.heading(materia["nombre"], size="4"),
            rx.badge(materia["curso"], color_scheme="blue"),
            rx.text(materia["descripcion"], size="2"),
            # Mejora técnica: El botón también debe ser dinámico sin f-strings de Python
            rx.button(
                "Comprar ", materia["precio"], "€", 
                width="100%", color_scheme="iris"
            ),
        
            spacing="1",
            align="start",
        ),
        width="18em",
        padding="1.5em",
        # Efecto visual: un borde sutil que resalta la tecnología
        border=f"1px solid {rx.color('iris', 5)}",
    ),

def index() -> rx.Component:
    return rx.vstack(
        navbar(),
        rx.container(
            # Título dinámico compatible con Reflex
            rx.heading("Apoyo Escolar para ", State.filtro_curso, margin_y="1em"),
            rx.hstack(
                rx.button("Todos", on_click=lambda: State.set_filtro("Todos")),
                rx.button("1º ESO", on_click=lambda: State.set_filtro("1º ESO")),
                rx.button("2º ESO", on_click=lambda: State.set_filtro("2º ESO")),
                rx.button("3º ESO", on_click=lambda: State.set_filtro("3º ESO")),
                rx.button("4º ESO", on_click=lambda: State.set_filtro("4º ESO")),
                rx.button("1º Bach", on_click=lambda: State.set_filtro("1º Bachillerato")),
                rx.button("2º Bach", on_click=lambda: State.set_filtro("2º Bachillerato")),
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