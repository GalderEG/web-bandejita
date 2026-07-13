import csv
import requests

CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSfR6ILf3cDq51hVw-GBANJ1wpfH5NrKgBgPvaYMAUeSiWLpWUCsCPJIkA5m-Ok1E7NpPtJtLzfAURH/pub?gid=0&single=true&output=csv"

def build_html():
    response = requests.get(CSV_URL)
    response.encoding = 'utf-8'
    if response.status_code != 200:
        print("Error descargando el CSV")
        return
        
    lineas = response.text.splitlines()
    lector = csv.reader(lineas)
    filas = list(lector)
    
    if len(filas) <= 1:
        return

    # Configuración global desde la fila 2 (índice 1)
    try:
        tasa_bcv = float(filas[1][8].replace(',', '.').strip())
    except:
        tasa_bcv = 1.0

    modo_moneda = 'bs'
    if len(filas[1]) > 6:
        moneda_str = filas[1][6].strip().lower()
        if moneda_str == 'usd':
            modo_moneda = 'usd'
        elif moneda_str == 'cop':
            modo_moneda = 'cop'

    menu_por_categoria = {}
    bloque_horarios = []
    bloque_testimonios = []
    bloque_blog = []

    for index, fila in enumerate(filas):
        if index == 0 or not fila[0]: 
            continue
            
        nombre = fila[0].strip()
        descripcion = fila[1].strip()
        precio_raw = fila[2].strip()
        categoria = fila[3].strip()
        disponible = fila[4].strip().lower()
        
        if disponible != 'si':
            continue

        cat_lower = categoria.lower()
        if cat_lower == 'horarios':
            bloque_horarios.append({"dias": nombre, "horas": descripcion})
            continue
        elif cat_lower == 'testimonios':
            bloque_testimonios.append({"autor": nombre, "texto": descripcion, "estrellas": precio_raw})
            continue
        elif cat_lower == 'blog':
            bloque_blog.append({"titulo": nombre, "texto": descripcion, "fecha": precio_raw})
            continue
        elif cat_lower == 'noticias':
            continue

        # Procesamiento financiero (soporta bs, usd y cop)
        try:
            limpio = precio_raw.replace('$', '').replace(',', '.')
            precio_usd = float(limpio)
            if modo_moneda == 'usd':
                precio_final = f"${precio_usd:.2f}".replace('.00', '')
            elif modo_moneda == 'cop':
                precio_final = f"COP {(precio_usd * tasa_bcv):,.0f}"
            else:
                precio_final = f"Bs { (precio_usd * tasa_bcv):.2f}"
        except:
            precio_final = f"${precio_raw}"

        if categoria not in menu_por_categoria:
            menu_por_categoria[categoria] = []
            
        menu_por_categoria[categoria].append({
            "nombre": nombre,
            "descripcion": descripcion,
            "precio": precio_final
        })

    html_content = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Menú, Horarios y Historias | Bandejita De Lata San Cristóbal</title>
    <meta name="description" content="Carta de platos activos, opiniones de clientes, horarios de atención en la Urb. Mérida y reflexiones de cocina en Bandejita de Lata.">
    <style>
        body { font-family: sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; color: #333; line-height: 1.6; }
        .banner-aviso { background: #f4f8f0; border: 1px solid #96b754; padding: 15px; border-radius: 8px; margin-bottom: 30px; text-align: center; }
        .banner-aviso a { color: #135c96; font-weight: bold; text-decoration: underline; }
        h1, h2, h3 { color: #135c96; }
        h1 { text-align: center; border-bottom: 3px solid #135c96; padding-bottom: 10px; }
        .categoria-bloque { margin-top: 40px; border-bottom: 2px solid #96b754; padding-bottom: 5px; }
        .item-row { margin: 20px 0; padding-left: 15px; border-left: 3px solid #135c96; }
        .item-header { display: flex; justify-content: space-between; font-weight: bold; }
        .item-desc { color: #555; font-size: 0.95rem; margin-top: 5px; text-align: justify; white-space: pre-wrap; }
        .meta-info { font-size: 0.8rem; color: #888; font-style: italic; }
    </style>
</head>
<body>

    <div class="banner-aviso">
        <p><strong>Versión de Lectura Directa:</strong> Este mapa de contenido está optimizado para motores de búsqueda. Para verificar disponibilidad de stock en tiempo real, ver imágenes o gestionar pedidos por WhatsApp, ingresa a nuestro <a href="index.html">Menú Digital Interactivo de Bandejita de Lata</a>.</p>
    </div>

    <h1>Bandejita De Lata — Resumen de Contenidos</h1>
"""

    html_content += "\n    <h2>Nuestra Carta Activa</h2>"
    for cat, platos in menu_por_categoria.items():
        html_content += f'\n    <div class="categoria-bloque">\n        <h3>{cat}</h3>\n    </div>\n'
        for p in platos:
            html_content += f"""    <div class="item-row">
        <div class="item-header">
            <span>{p['nombre']}</span>
            <span>{p['precio']}</span>
        </div>
        <p class="item-desc">{p['descripcion']}</p>
    </div>\n"""

    if bloque_horarios:
        html_content += "\n    <div class=\"categoria-bloque\">\n        <h2>Horarios de Atención</h2>\n    </div>\n"
        for h in bloque_horarios:
            html_content += f"""    <div class="item-row">
        <div class="item-header">
            <span>{h['dias']}</span>
            <span>{h['horas']}</span>
        </div>
    </div>\n"""

    if bloque_testimonios:
        html_content += "\n    <div class=\"categoria-bloque\">\n        <h2>Lo que dicen nuestros comensales</h2>\n    </div>\n"
        for t in bloque_testimonios:
            html_content += f"""    <div class="item-row">
        <div class="item-header">
            <span>{t['autor']}</span>
            <span style="color: #96b754;">{t['estrellas']}</span>
        </div>
        <p class="item-desc">"{t['texto']}"</p>
    </div>\n"""

    if bloque_blog:
        html_content += "\n    <div class=\"categoria-bloque\">\n        <h2>Aguamiel Con Leche — Reflexiones del Cocinero</h2>\n    </div>\n"
        for b in bloque_blog:
            html_content += f"""    <div class="item-row">
        <div class="item-header">
            <span>{b['titulo']}</span>
            <span class="meta-info">Publicado el: {b['fecha']}</span>
        </div>
        <p class="item-desc">{b['texto']}</p>
    </div>\n"""

    html_content += """
</body>
</html>"""

    with open("menu-estatico.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print("menu-estatico.html compilado con éxito.")

if __name__ == "__main__":
    build_html()
