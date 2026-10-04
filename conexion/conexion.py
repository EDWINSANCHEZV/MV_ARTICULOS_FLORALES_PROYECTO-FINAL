"""Conexión centralizada para SQLite y MySQL.

SQLite permite ejecutar el proyecto inmediatamente. Para la demostración con
MySQL, establezca DB_ENGINE=mysql y las variables MYSQL_* indicadas en README.
"""

import sqlite3
from pathlib import Path

from flask import current_app


def _es_mysql():
    return current_app.config.get("DB_ENGINE") == "mysql"


def get_connection():
    if _es_mysql():
        import mysql.connector
        return mysql.connector.connect(
            host=current_app.config["MYSQL_HOST"],
            port=current_app.config["MYSQL_PORT"],
            user=current_app.config["MYSQL_USER"],
            password=current_app.config["MYSQL_PASSWORD"],
            database=current_app.config["MYSQL_DATABASE"],
        )
    ruta = Path(current_app.config["DATABASE"])
    ruta.parent.mkdir(parents=True, exist_ok=True)
    conexion = sqlite3.connect(ruta)
    conexion.row_factory = sqlite3.Row
    conexion.execute("PRAGMA foreign_keys = ON")
    return conexion


def query_db(sql, parametros=(), one=False, commit=False, return_id=False):
    conexion = get_connection()
    cursor = None
    try:
        if _es_mysql():
            sql = sql.replace("?", "%s")
            cursor = conexion.cursor(dictionary=True)
        else:
            cursor = conexion.cursor()
        cursor.execute(sql, parametros)
        if commit:
            conexion.commit()
        if return_id:
            return cursor.lastrowid
        if cursor.description:
            filas = cursor.fetchall()
            return (filas[0] if filas else None) if one else filas
        return None
    finally:
        if cursor is not None:
            cursor.close()
        conexion.close()


def init_db():
    conexion = get_connection()
    try:
        nombre = "esquema_mysql.sql" if _es_mysql() else "esquema.sql"
        esquema = (Path(current_app.root_path) / "sql" / nombre).read_text(encoding="utf-8")
        if _es_mysql():
            cursor = conexion.cursor()
            for sentencia in esquema.split(";"):
                if sentencia.strip():
                    cursor.execute(sentencia)
            cursor.close()
        else:
            conexion.executescript(esquema)
        conexion.commit()
    finally:
        conexion.close()


def seed_db():
    """Crea datos de demostración solamente si las tablas están vacías."""
    if query_db("SELECT COUNT(*) AS total FROM proveedores", one=True)["total"] == 0:
        for datos in (
            ("Empaques Andinos", "María López", "0991112233", "ventas@empaquesandinos.ec", "Quito"),
            ("Papeles Ecuador", "Carlos Vega", "0982223344", "contacto@papelesecuador.ec", "Guayaquil"),
            ("Insumos Florícolas", "Andrea Ruiz", "0973334455", "info@insumosfloricolas.ec", "Cayambe"),
        ):
            query_db("INSERT INTO proveedores (empresa, contacto, telefono, correo, ciudad) VALUES (?, ?, ?, ?, ?)", datos, commit=True)

    if query_db("SELECT COUNT(*) AS total FROM clientes", one=True)["total"] == 0:
        for datos in (
            ("Florícola San Miguel", "1790010010001", "0994445566", "compras@sanmiguel.ec", "Tabacundo", 1),
            ("Detalles Primavera", "1712345678", "0985556677", "hola@primavera.ec", "Quito", 1),
            ("Rosas del Norte", "1790020020001", "0976667788", "ventas@rosasnorte.ec", "Cayambe", 1),
        ):
            query_db("INSERT INTO clientes (nombre, identificacion, telefono, correo, ciudad, activo) VALUES (?, ?, ?, ?, ?, ?)", datos, commit=True)

    if query_db("SELECT COUNT(*) AS total FROM productos", one=True)["total"] == 0:
        proveedores = query_db("SELECT id FROM proveedores ORDER BY id")
        productos = (
            ("Papel floral", "Papel decorativo para bouquets y arreglos florales.", "Papel floral", 18.50, 24, "producto_1.png", proveedores[1]["id"]),
            ("Malla protectora", "Malla para proteger las flores durante cultivo y transporte.", "Mallas", 12.75, 15, "producto_2.png", proveedores[2]["id"]),
            ("Fundas para rosas", "Fundas plásticas para proteger y presentar las rosas.", "Empaques", 9.90, 30, "producto_3.png", proveedores[0]["id"]),
        )
        for datos in productos:
            query_db("""INSERT INTO productos
                      (nombre, descripcion, categoria, precio, stock, imagen, proveedor_id)
                      VALUES (?, ?, ?, ?, ?, ?, ?)""", datos, commit=True)
