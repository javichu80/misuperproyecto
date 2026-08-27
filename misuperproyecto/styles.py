import reflex as rx

# 1. Definición de la Paleta de Colores y Constantes
COLOR_BLANCO_PURO = "#FFFFFF"
COLOR_BRANDNAME = "#E5E6ED"
COLOR_FONDO = "radial-gradient(circle at top,#334155 0%,#1e293b 20%,#0f172a 55%,#020617 100%)"
COLOR_PRIMARIO = 'indigo' 
COLOR_SECUNDARIO = "white"

COLOR_PANEL = "rgba(15,23,42,0.85)"

COLOR_CARD = "rgba(30,41,59,0.90)"

COLOR_TEXTO = "#F8FAFC"

COLOR_TEXTO_SECUNDARIO = "#CBD5E1"

COLOR_BORDE = "rgba(255,255,255)"

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

