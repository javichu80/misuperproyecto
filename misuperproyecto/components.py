import reflex as rx
from rxconfig import config
from .state import State
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

def card_materia(materia: dict) -> rx.Component:
    return rx.card(
        rx.vstack(
            # SOLUCIÓN: Usamos rx.cond para elegir el icono con un texto fijo
            rx.cond(
                materia["icono"] == "atom",
                rx.icon(tag="atom", size=30, color=rx.color(COLOR_PRIMARIO, 11)),
                rx.cond(
                    materia["icono"] == "bot",
                    rx.icon(tag="bot", size=30, color=rx.color(COLOR_PRIMARIO, 11)),
                        rx.cond(
                            materia["icono"] == "calculator",
                            rx.icon(tag="calculator", size=30, color=rx.color(COLOR_PRIMARIO, 11)),
                                rx.cond(
                                    materia["icono"] == "magnet",
                                    rx.icon(tag="magnet", size=30, color=rx.color(COLOR_PRIMARIO, 11)),
                                        rx.cond(
                                            materia["icono"] == "cpu",
                                            rx.icon(tag="cpu", size=30, color=rx.color(COLOR_PRIMARIO, 11)),
                                                rx.cond(
                                                    materia["icono"] == "settings",
                                                    rx.icon(tag="settings", size=30, color=rx.color(COLOR_PRIMARIO, 11)),
                                                        rx.cond(
                                                            materia["icono"] == "flask-conical", # <--- ¿Coincide este texto con state.py?
                                                            rx.icon(tag="flask-conical", size=30, color=rx.color(COLOR_PRIMARIO, 11)),
                                                                rx.cond(
                                                                    materia["icono"] == "layout_grid", # <--- ¿Coincide este texto con state.py?
                                                                    rx.icon(tag="layout-grid", size=30, color=rx.color(COLOR_PRIMARIO, 11)),
                                                                    # ICONO POR DEFECTO: Siempre debe haber un cierre
                                                                    rx.icon(tag="book-open", size=30, color=rx.color(COLOR_PRIMARIO, 11))
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
            rx.badge(materia["curso"], color_scheme="orange"),
            rx.text(materia["descripcion"], size="2"),
            # Mejora técnica: El botón también debe ser dinámico sin f-strings de Python
            rx.button(
                "Comprar ", materia["precio"], "€", 
                style = estilo_boton_compra
            ),
        
            spacing="1",
            align="start",
        ),
        style = estilo_base_tarjeta
    ),