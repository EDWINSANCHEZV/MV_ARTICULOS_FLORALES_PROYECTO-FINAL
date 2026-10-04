"""Aplicación final del Proyecto Integrador MV Artículos Florales."""

import os
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path
from urllib.parse import urljoin, urlparse

from flask import Flask, flash, redirect, render_template, request, url_for
from flask_login import LoginManager, UserMixin, current_user, login_required, login_user, logout_user
from flask_wtf.csrf import CSRFProtect
from werkzeug.security import check_password_hash, generate_password_hash

from conexion.conexion import init_db, query_db, seed_db
from forms.auth_form import LoginForm, RegistroForm
from forms.cliente_form import ClienteForm
from forms.facturacion_form import FacturaForm
from forms.producto_form import ProductoForm
from forms.proveedor_form import ProveedorForm
from forms.shared import EliminarForm


BASE_DIR = Path(__file__).resolve().parent
login_manager = LoginManager()
csrf = CSRFProtect()


@dataclass
class Usuario(UserMixin):
    id: int
    nombre: str
    usuario: str
    correo: str

    @classmethod
    def desde_fila(cls, fila):
        return cls(fila["id"], fila["nombre"], fila["usuario"], fila["correo"])


def crear_app(configuracion_pruebas=None):
    app = Flask(__name__)
    app.config.update(
        SECRET_KEY=os.getenv("SECRET_KEY", "clave-local-cambiar-en-produccion"),
        DB_ENGINE=os.getenv("DB_ENGINE", "sqlite").lower(),
        DATABASE=os.getenv("DATABASE_PATH", str(BASE_DIR / "data" / "mv_florales.db")),
        MYSQL_HOST=os.getenv("MYSQL_HOST", "localhost"),
        MYSQL_PORT=int(os.getenv("MYSQL_PORT", "3306")),
        MYSQL_USER=os.getenv("MYSQL_USER", "root"),
        MYSQL_PASSWORD=os.getenv("MYSQL_PASSWORD", ""),
        MYSQL_DATABASE=os.getenv("MYSQL_DATABASE", "mv_articulos_florales"),
    )
    if configuracion_pruebas:
        app.config.update(configuracion_pruebas)

    csrf.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "login"
    login_manager.login_message = "Inicie sesión para acceder al sistema."
    login_manager.login_message_category = "warning"

    @login_manager.user_loader
    def cargar_usuario(usuario_id):
        fila = query_db(
            "SELECT id, nombre, usuario, correo FROM usuarios WHERE id = ?",
            (usuario_id,), one=True,
        )
        return Usuario.desde_fila(fila) if fila else None

    def destino_seguro(destino):
        if not destino:
            return False
        referencia = urlparse(request.host_url)
        prueba = urlparse(urljoin(request.host_url, destino or ""))
        return prueba.scheme in ("http", "https") and referencia.netloc == prueba.netloc

    @app.route("/")
    def inicio():
        destacados = query_db(
            """
            SELECT p.id, p.nombre, p.descripcion, p.categoria, p.precio, p.stock,
                   p.imagen, pr.empresa AS proveedor
            FROM productos p
            LEFT JOIN proveedores pr ON pr.id = p.proveedor_id
            ORDER BY p.id DESC LIMIT 3
            """
        )
        return render_template("index.html", productos=destacados)

    @app.route("/registro", methods=["GET", "POST"])
    def registro():
        if current_user.is_authenticated:
            return redirect(url_for("panel"))
        form = RegistroForm()
        if form.validate_on_submit():
            existente = query_db(
                "SELECT id FROM usuarios WHERE usuario = ? OR correo = ?",
                (form.usuario.data.strip(), form.correo.data.lower().strip()), one=True,
            )
            if existente:
                flash("El usuario o correo ya se encuentra registrado.", "danger")
            else:
                query_db(
                    "INSERT INTO usuarios (nombre, usuario, correo, password_hash) VALUES (?, ?, ?, ?)",
                    (form.nombre.data.strip(), form.usuario.data.strip(), form.correo.data.lower().strip(),
                     generate_password_hash(form.password.data)), commit=True,
                )
                flash("Usuario registrado correctamente. Ya puede iniciar sesión.", "success")
                return redirect(url_for("login"))
        return render_template("auth/registro.html", form=form)

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for("panel"))
        form = LoginForm()
        if form.validate_on_submit():
            fila = query_db("SELECT * FROM usuarios WHERE usuario = ?", (form.usuario.data.strip(),), one=True)
            if fila and check_password_hash(fila["password_hash"], form.password.data):
                login_user(Usuario.desde_fila(fila), remember=form.recordarme.data)
                flash(f"Bienvenido, {fila['nombre']}.", "success")
                siguiente = request.args.get("next")
                return redirect(siguiente if destino_seguro(siguiente) else url_for("panel"))
            flash("Usuario o contraseña incorrectos.", "danger")
        return render_template("auth/login.html", form=form)

    @app.post("/logout")
    @login_required
    def logout():
        if EliminarForm().validate_on_submit():
            logout_user()
            flash("La sesión se cerró correctamente.", "info")
        return redirect(url_for("inicio"))

    @app.route("/panel")
    @login_required
    def panel():
        estadisticas = {
            "productos": query_db("SELECT COUNT(*) AS total FROM productos", one=True)["total"],
            "clientes": query_db("SELECT COUNT(*) AS total FROM clientes", one=True)["total"],
            "proveedores": query_db("SELECT COUNT(*) AS total FROM proveedores", one=True)["total"],
            "facturas": query_db("SELECT COUNT(*) AS total FROM facturas", one=True)["total"],
        }
        ultimas = query_db(
            """SELECT f.id, f.numero, f.fecha, f.total, f.estado, c.nombre AS cliente
               FROM facturas f JOIN clientes c ON c.id = f.cliente_id
               ORDER BY f.id DESC LIMIT 5"""
        )
        return render_template("panel.html", estadisticas=estadisticas, facturas=ultimas)

    def opciones_proveedores(form):
        filas = query_db("SELECT id, empresa FROM proveedores ORDER BY empresa")
        form.proveedor_id.choices = [(0, "Sin proveedor asignado")] + [(x["id"], x["empresa"]) for x in filas]

    @app.route("/productos")
    @login_required
    def productos():
        filas = query_db(
            """SELECT p.*, pr.empresa AS proveedor FROM productos p
               LEFT JOIN proveedores pr ON pr.id = p.proveedor_id ORDER BY p.nombre"""
        )
        return render_template("productos.html", productos=filas, eliminar_form=EliminarForm())

    @app.route("/productos/nuevo", methods=["GET", "POST"])
    @login_required
    def producto_nuevo():
        form = ProductoForm()
        opciones_proveedores(form)
        if form.validate_on_submit():
            query_db(
                """INSERT INTO productos
                   (nombre, descripcion, categoria, precio, stock, imagen, proveedor_id)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (form.nombre.data.strip(), form.descripcion.data.strip(), form.categoria.data,
                 float(form.precio.data), form.stock.data, form.imagen.data.strip() or "producto_1.png",
                 form.proveedor_id.data or None), commit=True,
            )
            flash("Producto registrado correctamente.", "success")
            return redirect(url_for("productos"))
        return render_template("formulario_producto.html", form=form, titulo="Nuevo producto")

    @app.route("/productos/<int:producto_id>/editar", methods=["GET", "POST"])
    @login_required
    def producto_editar(producto_id):
        producto = query_db("SELECT * FROM productos WHERE id = ?", (producto_id,), one=True)
        if not producto:
            flash("Producto no encontrado.", "danger")
            return redirect(url_for("productos"))
        form = ProductoForm(data=dict(producto))
        opciones_proveedores(form)
        if request.method == "GET":
            form.proveedor_id.data = producto["proveedor_id"] or 0
        if form.validate_on_submit():
            query_db(
                """UPDATE productos SET nombre=?, descripcion=?, categoria=?, precio=?, stock=?,
                   imagen=?, proveedor_id=? WHERE id=?""",
                (form.nombre.data.strip(), form.descripcion.data.strip(), form.categoria.data,
                 float(form.precio.data), form.stock.data, form.imagen.data.strip() or "producto_1.png",
                 form.proveedor_id.data or None, producto_id), commit=True,
            )
            flash("Producto actualizado correctamente.", "success")
            return redirect(url_for("productos"))
        return render_template("formulario_producto.html", form=form, titulo="Editar producto")

    @app.post("/productos/<int:producto_id>/eliminar")
    @login_required
    def producto_eliminar(producto_id):
        if EliminarForm().validate_on_submit():
            usado = query_db("SELECT id FROM detalle_factura WHERE producto_id = ? LIMIT 1", (producto_id,), one=True)
            if usado:
                flash("No se puede eliminar: el producto aparece en una factura.", "warning")
            else:
                query_db("DELETE FROM productos WHERE id = ?", (producto_id,), commit=True)
                flash("Producto eliminado.", "success")
        return redirect(url_for("productos"))

    @app.route("/clientes")
    @login_required
    def clientes():
        return render_template("clientes.html", clientes=query_db("SELECT * FROM clientes ORDER BY nombre"),
                               eliminar_form=EliminarForm())

    @app.route("/clientes/nuevo", methods=["GET", "POST"])
    @login_required
    def cliente_nuevo():
        form = ClienteForm()
        if form.validate_on_submit():
            query_db(
                """INSERT INTO clientes (nombre, identificacion, telefono, correo, ciudad, activo)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (form.nombre.data.strip(), form.identificacion.data.strip(), form.telefono.data.strip(),
                 form.correo.data.lower().strip(), form.ciudad.data.strip(), int(form.activo.data)), commit=True,
            )
            flash("Cliente registrado correctamente.", "success")
            return redirect(url_for("clientes"))
        return render_template("formulario_cliente.html", form=form, titulo="Nuevo cliente")

    @app.route("/clientes/<int:cliente_id>/editar", methods=["GET", "POST"])
    @login_required
    def cliente_editar(cliente_id):
        cliente = query_db("SELECT * FROM clientes WHERE id = ?", (cliente_id,), one=True)
        if not cliente:
            flash("Cliente no encontrado.", "danger")
            return redirect(url_for("clientes"))
        form = ClienteForm(data=dict(cliente))
        if form.validate_on_submit():
            query_db(
                """UPDATE clientes SET nombre=?, identificacion=?, telefono=?, correo=?, ciudad=?, activo=?
                   WHERE id=?""",
                (form.nombre.data.strip(), form.identificacion.data.strip(), form.telefono.data.strip(),
                 form.correo.data.lower().strip(), form.ciudad.data.strip(), int(form.activo.data), cliente_id), commit=True,
            )
            flash("Cliente actualizado correctamente.", "success")
            return redirect(url_for("clientes"))
        return render_template("formulario_cliente.html", form=form, titulo="Editar cliente")

    @app.post("/clientes/<int:cliente_id>/eliminar")
    @login_required
    def cliente_eliminar(cliente_id):
        if EliminarForm().validate_on_submit():
            usado = query_db("SELECT id FROM facturas WHERE cliente_id = ? LIMIT 1", (cliente_id,), one=True)
            if usado:
                flash("No se puede eliminar: el cliente tiene facturas registradas.", "warning")
            else:
                query_db("DELETE FROM clientes WHERE id = ?", (cliente_id,), commit=True)
                flash("Cliente eliminado.", "success")
        return redirect(url_for("clientes"))

    @app.route("/proveedores")
    @login_required
    def proveedores():
        return render_template("proveedores.html", proveedores=query_db("SELECT * FROM proveedores ORDER BY empresa"),
                               eliminar_form=EliminarForm())

    @app.route("/proveedores/nuevo", methods=["GET", "POST"])
    @login_required
    def proveedor_nuevo():
        form = ProveedorForm()
        if form.validate_on_submit():
            query_db(
                """INSERT INTO proveedores (empresa, contacto, telefono, correo, ciudad)
                   VALUES (?, ?, ?, ?, ?)""",
                (form.empresa.data.strip(), form.contacto.data.strip(), form.telefono.data.strip(),
                 form.correo.data.lower().strip(), form.ciudad.data.strip()), commit=True,
            )
            flash("Proveedor registrado correctamente.", "success")
            return redirect(url_for("proveedores"))
        return render_template("formulario_proveedor.html", form=form, titulo="Nuevo proveedor")

    @app.route("/proveedores/<int:proveedor_id>/editar", methods=["GET", "POST"])
    @login_required
    def proveedor_editar(proveedor_id):
        proveedor = query_db("SELECT * FROM proveedores WHERE id = ?", (proveedor_id,), one=True)
        if not proveedor:
            flash("Proveedor no encontrado.", "danger")
            return redirect(url_for("proveedores"))
        form = ProveedorForm(data=dict(proveedor))
        if form.validate_on_submit():
            query_db(
                "UPDATE proveedores SET empresa=?, contacto=?, telefono=?, correo=?, ciudad=? WHERE id=?",
                (form.empresa.data.strip(), form.contacto.data.strip(), form.telefono.data.strip(),
                 form.correo.data.lower().strip(), form.ciudad.data.strip(), proveedor_id), commit=True,
            )
            flash("Proveedor actualizado correctamente.", "success")
            return redirect(url_for("proveedores"))
        return render_template("formulario_proveedor.html", form=form, titulo="Editar proveedor")

    @app.post("/proveedores/<int:proveedor_id>/eliminar")
    @login_required
    def proveedor_eliminar(proveedor_id):
        if EliminarForm().validate_on_submit():
            usado = query_db("SELECT id FROM productos WHERE proveedor_id = ? LIMIT 1", (proveedor_id,), one=True)
            if usado:
                flash("No se puede eliminar: el proveedor tiene productos asociados.", "warning")
            else:
                query_db("DELETE FROM proveedores WHERE id = ?", (proveedor_id,), commit=True)
                flash("Proveedor eliminado.", "success")
        return redirect(url_for("proveedores"))

    def opciones_factura(form):
        clientes_db = query_db("SELECT id, nombre FROM clientes WHERE activo = 1 ORDER BY nombre")
        productos_db = query_db("SELECT id, nombre, precio, stock FROM productos ORDER BY nombre")
        form.cliente_id.choices = [(x["id"], x["nombre"]) for x in clientes_db]
        form.producto_id.choices = [
            (x["id"], f"{x['nombre']} · ${float(x['precio']):.2f} · stock {x['stock']}") for x in productos_db
        ]

    @app.route("/facturacion")
    @login_required
    def facturacion():
        filas = query_db(
            """SELECT f.id, f.numero, f.fecha, f.total, f.estado, c.nombre AS cliente,
                      p.nombre AS producto, d.cantidad, d.precio_unitario
               FROM facturas f JOIN clientes c ON c.id = f.cliente_id
               JOIN detalle_factura d ON d.factura_id = f.id
               JOIN productos p ON p.id = d.producto_id ORDER BY f.id DESC"""
        )
        total = sum(Decimal(str(f["total"])) for f in filas)
        return render_template("facturacion.html", facturas=filas, total_facturado=total,
                               eliminar_form=EliminarForm())

    @app.route("/facturacion/nueva", methods=["GET", "POST"])
    @login_required
    def factura_nueva():
        form = FacturaForm()
        opciones_factura(form)
        if form.validate_on_submit():
            producto = query_db("SELECT precio, stock FROM productos WHERE id = ?", (form.producto_id.data,), one=True)
            if not producto or producto["stock"] < form.cantidad.data:
                flash("La cantidad solicitada supera el stock disponible.", "warning")
            else:
                siguiente = query_db("SELECT COALESCE(MAX(id), 0) + 1 AS numero FROM facturas", one=True)["numero"]
                numero = f"FAC-{siguiente:04d}"
                total = float(producto["precio"]) * form.cantidad.data
                factura_id = query_db(
                    "INSERT INTO facturas (numero, cliente_id, total, estado) VALUES (?, ?, ?, ?)",
                    (numero, form.cliente_id.data, total, form.estado.data), commit=True, return_id=True,
                )
                query_db(
                    "INSERT INTO detalle_factura (factura_id, producto_id, cantidad, precio_unitario) VALUES (?, ?, ?, ?)",
                    (factura_id, form.producto_id.data, form.cantidad.data, float(producto["precio"])), commit=True,
                )
                query_db("UPDATE productos SET stock = stock - ? WHERE id = ?",
                         (form.cantidad.data, form.producto_id.data), commit=True)
                flash(f"Factura {numero} registrada correctamente.", "success")
                return redirect(url_for("facturacion"))
        return render_template("formulario_facturacion.html", form=form, titulo="Nueva factura")

    @app.route("/facturacion/<int:factura_id>/editar", methods=["GET", "POST"])
    @login_required
    def factura_editar(factura_id):
        factura = query_db(
            """SELECT f.*, d.producto_id, d.cantidad FROM facturas f
               JOIN detalle_factura d ON d.factura_id=f.id WHERE f.id=?""", (factura_id,), one=True,
        )
        if not factura:
            flash("Factura no encontrada.", "danger")
            return redirect(url_for("facturacion"))
        form = FacturaForm(data=dict(factura))
        opciones_factura(form)
        if request.method == "GET":
            form.cliente_id.data = factura["cliente_id"]
            form.producto_id.data = factura["producto_id"]
            form.cantidad.data = factura["cantidad"]
            form.estado.data = factura["estado"]
        if form.validate_on_submit():
            producto = query_db("SELECT precio, stock FROM productos WHERE id=?", (form.producto_id.data,), one=True)
            disponible = (producto["stock"] if producto else 0) + (
                factura["cantidad"] if form.producto_id.data == factura["producto_id"] else 0
            )
            if not producto or disponible < form.cantidad.data:
                flash("La cantidad solicitada supera el stock disponible.", "warning")
            else:
                query_db("UPDATE productos SET stock=stock+? WHERE id=?",
                         (factura["cantidad"], factura["producto_id"]), commit=True)
                total = float(producto["precio"]) * form.cantidad.data
                query_db("UPDATE facturas SET cliente_id=?, total=?, estado=? WHERE id=?",
                         (form.cliente_id.data, total, form.estado.data, factura_id), commit=True)
                query_db("UPDATE detalle_factura SET producto_id=?, cantidad=?, precio_unitario=? WHERE factura_id=?",
                         (form.producto_id.data, form.cantidad.data, float(producto["precio"]), factura_id), commit=True)
                query_db("UPDATE productos SET stock=stock-? WHERE id=?",
                         (form.cantidad.data, form.producto_id.data), commit=True)
                flash("Factura actualizada correctamente.", "success")
                return redirect(url_for("facturacion"))
        return render_template("formulario_facturacion.html", form=form, titulo="Editar factura")

    @app.post("/facturacion/<int:factura_id>/eliminar")
    @login_required
    def factura_eliminar(factura_id):
        if EliminarForm().validate_on_submit():
            detalle = query_db("SELECT producto_id, cantidad FROM detalle_factura WHERE factura_id=?", (factura_id,), one=True)
            if detalle:
                query_db("UPDATE productos SET stock=stock+? WHERE id=?",
                         (detalle["cantidad"], detalle["producto_id"]), commit=True)
            query_db("DELETE FROM facturas WHERE id=?", (factura_id,), commit=True)
            flash("Factura eliminada y stock restaurado.", "success")
        return redirect(url_for("facturacion"))

    @app.errorhandler(404)
    def no_encontrado(_error):
        return render_template("404.html"), 404

    with app.app_context():
        init_db()
        seed_db()

    return app


app = crear_app()


if __name__ == "__main__":
    app.run(debug=os.getenv("FLASK_DEBUG", "0") == "1")
