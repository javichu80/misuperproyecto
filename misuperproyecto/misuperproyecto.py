import reflex as rx
from .components import navbar
from .state import State

def card_materia(materia: dict) -> rx.Component:
    return rx.card(
        rx.vstack(
            # Acceso profesional por clave de diccionario
            rx.heading(materia["nombre"], size="4"),
            rx.badge(materia["curso"], color_scheme="blue"),
            rx.text(materia["descripcion"], size="2"),
            rx.button(f"Comprar {materia['precio']}€", width="100%"),
            spacing="2", align="start",
        ),
        width="18em",
    )

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