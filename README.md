# MV Artículos Florales — Proyecto final Semana 16

Sistema web desarrollado con Python, Flask, Jinja2, Bootstrap, Flask-WTF y Flask-Login. El proyecto continúa los avances de las semanas 10 a 14 y cumple la evaluación final de la Semana 16.

## Funcionalidades terminadas

- Registro e inicio de sesión de usuarios.
- Contraseñas protegidas mediante hash de Werkzeug.
- Sesiones y rutas privadas con Flask-Login.
- Formularios validados en el servidor con Flask-WTF y protección CSRF.
- CRUD completo de productos, clientes, proveedores y facturas.
- Base de datos relacional con cinco entidades y claves foráneas.
- Relación proveedor → productos y cliente → facturas → detalle → producto.
- Actualización automática del stock al crear, modificar o eliminar una factura.
- Diseño adaptable con Bootstrap 5.
- Compatibilidad con SQLite para demostración inmediata y MySQL para la defensa.

## Ejecución rápida en Windows

1. Descargue o clone el repositorio.
2. Abra la carpeta del proyecto.
3. Ejecute `iniciar.bat`.
4. Abra `http://127.0.0.1:5000`.
5. Cree una cuenta desde la pantalla **Registro** e inicie sesión.

También puede ejecutar manualmente:

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

La base SQLite y los datos iniciales se crean automáticamente en el primer inicio.

## Configuración con MySQL

1. Cree la base:

```sql
CREATE DATABASE mv_articulos_florales CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

2. Configure las variables del archivo `.env.example` en su sistema:

```text
DB_ENGINE=mysql
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=su_clave
MYSQL_DATABASE=mv_articulos_florales
SECRET_KEY=una_clave_segura
```

3. Ejecute `python app.py`. La aplicación usa `sql/esquema_mysql.sql` para crear las tablas y relaciones.

## Estructura principal

```text
app.py
conexion/conexion.py
forms/
sql/esquema.sql
sql/esquema_mysql.sql
templates/
static/
tests/
```

## Pruebas

```bash
pytest -q
```

## Nota sobre GitHub Pages

GitHub Pages solo ejecuta archivos estáticos y no puede procesar Flask, sesiones ni bases de datos. El código completo debe entregarse en GitHub y ejecutarse localmente para la demostración. El `index.html` de la raíz se conserva únicamente como vista estática complementaria.

Desarrollado por Edwin Sánchez — 2026.
