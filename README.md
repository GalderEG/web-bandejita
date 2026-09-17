# Bandejita De Lata — Web

Sitio web y PWA de **Bandejita De Lata** (cocina de autor, San Cristóbal, Táchira).

- **Sitio en vivo:** https://bandejitadelata.com
- **Tecnología:** HTML/CSS/JS estático + PWA (Service Worker). Publicado con GitHub Pages.

## Estructura

| Archivo | Descripción |
| --- | --- |
| `index.html` | Sitio interactivo principal. Lee el menú, horarios, testimonios y blog en vivo desde un Google Sheet (CSV publicado). |
| `menu-estatico.html` | Versión SEO de solo lectura, **generada automáticamente**. No editar a mano. |
| `generate_menu.py` | Script que genera `menu-estatico.html` a partir del Google Sheet. |
| `sw.js` | Service Worker de la PWA (network-first; nunca cachea el CSV). |
| `manifest.json` | Manifiesto de la PWA. |
| `CNAME` | Dominio propio para GitHub Pages. |
| `.github/workflows/update-static-menu.yml` | Workflow que regenera `menu-estatico.html`. |

## Contenido vs código

- **Contenido** (menú, precios, horarios, testimonios, blog): se edita en el
  **Google Sheet**. El cambio regenera `menu-estatico.html` automáticamente.
- **Código/diseño**: se editan los archivos y se publican con `git push` a `main`.

## Desarrollo local

```bash
cd web-bandejita
python3 -m http.server 8000
# abrir http://localhost:8000
```

## Publicar cambios

```bash
git add -A
git commit -m "descripcion del cambio"
git push origin main
```

GitHub Pages actualiza el sitio automáticamente en unos minutos.

> Al modificar `index.html` o recursos cacheados, subir la versión de
> `CACHE_NAME` en `sw.js` (p. ej. `bandejita-cache-v3` → `v4`).

## Documentación para agentes

Ver [`AGENTS.md`](AGENTS.md) para el flujo detallado de mantenimiento y la
configuración de autenticación git.
