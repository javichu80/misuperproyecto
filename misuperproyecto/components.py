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
            
            spacing="1",
            align="start",
        ),
        style=estilo_base_tarjeta
    )


def formulario_materia() -> rx.Component:
    return rx.vstack(
        rx.heading("Añadir Nueva Materia", size="5"),
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
        border=f"1px solid {rx.color('slate', 5)}",
        border_radius="15px",
        spacing="3",
        width="100%",
    )
