import reflex as rx

# 1. Definición de la Paleta de Colores y Constantes
COLOR_BLANCO_PURO = "#FFFFFF"
COLOR_BRANDNAME = "#E5E6ED"
COLOR_FONDO = "#1F3065"  # Un tono oscuro profundo para el modo "Dark STEM"
COLOR_PRIMARIO = 'indigo' 
COLOR_SECUNDARIO = "white"
COLOR_TEXTO = rx.color("slate", 12)

# 2. Estilos comunes reutilizables (DRY: Don't Repeat Yourself)
estilo_base_tarjeta = {
    "width": "100%", # Cambiado de 18em para que la grilla lo controle mejor
    "padding": "1.5em",
    "border_radius": "15px",
    "background": rx.color("slate", 2), # Fondo ligeramente distinto al de la web
    "border": f"1px solid {rx.color('slate', 4)}", # Borde fino por defecto
    "transition": "all 0.3s ease-in-out", # Transición más suave
    "_hover": {
        "transform": "translateY(-10px)", # Elevación un poco mayor
        # EFECTO GLOW (Brillo):
        "box_shadow": f"0px 10px 30px {rx.color(COLOR_PRIMARIO, 4)}",
        "border": f"1px solid {rx.color(COLOR_PRIMARIO, 7)}",
    },
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

