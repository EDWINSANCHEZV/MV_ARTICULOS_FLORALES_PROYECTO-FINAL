# MV Artículos Florales - Semana 10

Proyecto Integrador U3 - Avance 10/16: aplicación web con Python, Flask y contenido dinámico mediante Jinja2.

## Archivos principales

- `app.py`: aplicación Flask, rutas y datos temporales en listas y diccionarios.
- `templates/`: plantilla base, páginas internas y componentes reutilizables.
- `static/`: archivos CSS, JavaScript e imágenes usados por Flask.
- `index.html`, `css/`, `script.js` e `img/`: frontend estático conservado para GitHub Pages.
- `requirements.txt`: dependencia necesaria para ejecutar Flask.

## Rutas de Flask

- `/`: página principal.
- `/productos`: catálogo generado con un bucle `for`.
- `/clientes`: registros de clientes y estados condicionales.
- `/proveedores`: tarjetas dinámicas de proveedores.
- `/facturacion`: facturas, total calculado y estados de pago.

## Ejecución local

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Luego visite `http://127.0.0.1:5000`.

## Publicación

GitHub Pages se mantiene desde la rama `main` y la carpeta raíz para mostrar el frontend. Flask y Jinja2 se prueban localmente.
