import reflex as rx

# 1. Definición de la Paleta de Colores y Constantes
COLOR_FONDO = "#0F1117"  # Un tono oscuro profundo para el modo "Dark STEM"
COLOR_PRIMARIO = "yellow"
COLOR_SECUNDARIO = "orange"
COLOR_TEXTO = rx.color("slate", 12)

# 2. Estilos comunes reutilizables (DRY: Don't Repeat Yourself)
estilo_base_tarjeta = {
    "width": "18em",
    "padding": "1.5em",
    "border_radius": "15px",
    "transition": "all 0.2s ease-in-out",
    "_hover": {
        "transform": "translateY(-5px)",
        "box_shadow": f"10px 10px 20px {rx.color(COLOR_PRIMARIO, 3)}",
    }
}

estilo_boton_compra = {
    "width": "100%",
    "color_scheme": COLOR_PRIMARIO,
    "variant": "soft",
    "cursor": "pointer"
}

# 3. Estilos para los botones de filtrado (Centralizados)
# Separamos las propiedades fijas para que el archivo principal sea más corto
ESTILO_BOTON_FILTRO_BASE = {
    "size": "3",
    "transition": "all 0.3s ease",
    "border_radius": "10px",
}

