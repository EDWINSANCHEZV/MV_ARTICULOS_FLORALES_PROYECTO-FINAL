from app import crear_app
from conexion.conexion import query_db


def nueva_app(tmp_path):
    return crear_app({
        "TESTING": True,
        "WTF_CSRF_ENABLED": False,
        "DB_ENGINE": "sqlite",
        "DATABASE": str(tmp_path / "prueba.db"),
        "SECRET_KEY": "pruebas",
    })


def registrar_y_entrar(cliente):
    respuesta = cliente.post("/registro", data={
        "nombre": "Edwin Sánchez",
        "usuario": "edwin_test",
        "correo": "edwin@example.com",
        "password": "Segura123",
        "confirmar": "Segura123",
    }, follow_redirects=True)
    assert respuesta.status_code == 200
    return cliente.post("/login", data={"usuario": "edwin_test", "password": "Segura123"}, follow_redirects=True)


def test_inicio_registro_login_y_rutas_protegidas(tmp_path):
    app = nueva_app(tmp_path)
    cliente = app.test_client()
    assert cliente.get("/").status_code == 200
    assert cliente.get("/productos").status_code == 302
    respuesta = registrar_y_entrar(cliente)
    assert b"Panel principal" in respuesta.data
    assert cliente.get("/productos").status_code == 200


def test_crud_producto_y_factura_relacional(tmp_path):
    app = nueva_app(tmp_path)
    cliente = app.test_client()
    registrar_y_entrar(cliente)
    with app.app_context():
        proveedor = query_db("SELECT id FROM proveedores ORDER BY id LIMIT 1", one=True)
        comprador = query_db("SELECT id FROM clientes ORDER BY id LIMIT 1", one=True)
    respuesta = cliente.post("/productos/nuevo", data={
        "nombre": "Cinta floral verde",
        "descripcion": "Cinta profesional para tallos y arreglos florales.",
        "categoria": "Cintas",
        "precio": "3.50",
        "stock": "20",
        "imagen": "producto_1.png",
        "proveedor_id": str(proveedor["id"]),
    }, follow_redirects=True)
    assert b"Cinta floral verde" in respuesta.data
    with app.app_context():
        producto = query_db("SELECT id FROM productos WHERE nombre=?", ("Cinta floral verde",), one=True)
    respuesta = cliente.post("/facturacion/nueva", data={
        "cliente_id": str(comprador["id"]),
        "producto_id": str(producto["id"]),
        "cantidad": "2",
        "estado": "Pagada",
    }, follow_redirects=True)
    assert b"Pagada" in respuesta.data
    with app.app_context():
        stock = query_db("SELECT stock FROM productos WHERE id=?", (producto["id"],), one=True)
        assert stock["stock"] == 18
