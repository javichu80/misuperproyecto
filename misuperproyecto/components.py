import reflex as rx
from rxconfig import config
from .state import State


# Asegúrate de que esta función esté presente
def navbar() -> rx.Component:
    return rx.hstack(
        rx.heading(State.brand_name, size="7"),
        rx.spacer(),
        rx.link("Inicio", href="/", color="blue"),
        rx.link("Productos", href="/productos", color="gray"),
        # ... resto de estilos del navbar
    )
