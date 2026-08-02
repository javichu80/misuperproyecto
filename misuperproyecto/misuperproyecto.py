"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx

from rxconfig import config


class State(rx.State):
    """The app state."""


def index() -> rx.Component:
    # Welcome Page (Index)
    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.vstack(
            rx.heading("Bienvenido a la web de Javichu", size="9"),
            rx.text(
                "Construyendo un futuro mejor",
                rx.code(f"{config.app_name}/{config.app_name}.py"),
                size="5",
            ),
            rx.link(
                rx.button("Explora nuestro productos"),
                color_scheme="blue",
                on_click=rx.window_alert("Proximamente!")
            ),
            spacing="5",
            justify="center",
        ),
    )
app = rx.App()
app.add_page(index)
