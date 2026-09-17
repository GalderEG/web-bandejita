# AGENTS.md — web-bandejita

Sitio estático de **Bandejita De Lata** publicado con GitHub Pages en
https://bandejitadelata.com (dominio propio vía `CNAME`).

## Estructura

- `index.html` — sitio interactivo principal. Lee el menú/horarios/blog en vivo
  desde un Google Sheet publicado como CSV.
- `menu-estatico.html` — versión SEO generada automáticamente. **No editar a mano.**
- `generate_menu.py` — genera `menu-estatico.html` a partir del Google Sheet.
- `sw.js` — Service Worker (PWA). Estrategia network-first; nunca cachea el CSV.
- `manifest.json` — manifiesto PWA.
- `.github/workflows/update-static-menu.yml` — regenera `menu-estatico.html`
  (disparo `repository_dispatch: sheet_updated` o manual).

## Despliegue

GitHub Pages publica desde la rama `main` (raíz del repo). Al hacer `push` a
`main`, el sitio se actualiza solo en ~1–5 minutos (incluye caché de CDN).

## Autenticación git

Este clon usa una **deploy key** dedicada, no la llave personal.

- Llave: `~/.ssh/bandejita_deploy` (privada, solo esta máquina).
- Alias SSH: `github-bandejita` definido en `~/.ssh/config`.
- Remoto: `git@github-bandejita:GalderEG/web-bandejita.git`.

Verificar conexión:

```bash
ssh -T git@github-bandejita
```

## Flujo de mantenimiento

1. Entrar al repo: `cd /home/angel/web-bandejita`
2. Traer cambios: `git pull origin main`
3. Editar (código/diseño: `index.html`, `sw.js`, `manifest.json`).
4. Previsualizar en local:

   ```bash
   python3 -m http.server 8000
   # abrir http://localhost:8000
   ```

5. Publicar:

   ```bash
   git add -A
   git commit -m "descripcion del cambio"
   git push origin main
   ```

### Regla del Service Worker

Al modificar `index.html` (o cualquier recurso cacheado), subir la versión en
`sw.js`, p. ej. `bandejita-cache-v2` → `bandejita-cache-v3`, para forzar el
refresco en los dispositivos de los clientes.

## Contenido vs código

- **Menú, precios, horarios, testimonios y blog**: se editan en el **Google
  Sheet**. No requieren git; el cambio dispara el workflow y regenera
  `menu-estatico.html`.
- **Diseño, estilos y lógica**: se editan en `index.html` y se publican por git.

## Pendientes / mejoras opcionales

- Añadir disparo `push` al workflow para regenerar `menu-estatico.html` también
  al editar código.
- `sw.js` referencia una imagen por SHA fijo (commit `2c9e405`); conviene
  apuntarla a `main`.
- Ampliar el `README.md` (hoy solo tiene el título).
