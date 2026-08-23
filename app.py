from flask import Flask, render_template

app = Flask(__name__)


# Datos temporales del proyecto. En esta etapa no se utiliza una base de datos.
PRODUCTOS = [
    {
        "id": 1,
        "nombre": "Papel Floral",
        "descripcion": "Papel decorativo para envolver bouquets y arreglos florales.",
        "categoria": "Papel floral",
        "precio": 18.50,
        "stock": 24,
        "imagen": "producto_1.png",
    },
    {
        "id": 2,
        "nombre": "Malla Protectora",
        "descripcion": "Malla para proteger las flores durante el cultivo y transporte.",
        "categoria": "Mallas",
        "precio": 12.75,
        "stock": 15,
        "imagen": "producto_2.png",
    },
    {
        "id": 3,
        "nombre": "Fundas para Rosas",
        "descripcion": "Fundas plásticas que protegen y mejoran la presentación de las rosas.",
        "categoria": "Empaques",
        "precio": 9.90,
        "stock": 0,
        "imagen": "producto_3.png",
    },
]

CLIENTES = [
    {"nombre": "Florícola San Miguel", "ciudad": "Tabacundo", "tipo": "Florícola", "activo": True},
    {"nombre": "Detalles Primavera", "ciudad": "Quito", "tipo": "Floristería", "activo": True},
    {"nombre": "Rosas del Norte", "ciudad": "Cayambe", "tipo": "Exportadora", "activo": False},
]

PROVEEDORES = [
    {"empresa": "Empaques Andinos", "producto": "Fundas y empaques", "ciudad": "Quito", "entrega": 3},
    {"empresa": "Papeles Ecuador", "producto": "Papel floral", "ciudad": "Guayaquil", "entrega": 5},
    {"empresa": "Insumos Florícolas", "producto": "Mallas y cintas", "ciudad": "Cayambe", "entrega": 2},
]

FACTURAS = [
    {"numero": "FAC-001", "cliente": "Florícola San Miguel", "fecha": "15/08/2026", "total": 185.00, "pagada": True},
    {"numero": "FAC-002", "cliente": "Detalles Primavera", "fecha": "18/08/2026", "total": 96.50, "pagada": False},
    {"numero": "FAC-003", "cliente": "Rosas del Norte", "fecha": "21/08/2026", "total": 240.75, "pagada": True},
]


@app.route("/")
def inicio():
    empresa = {
        "nombre": "MV Artículos Florales",
        "lema": "Calidad y confianza para el cuidado de tus flores",
        "ubicacion": "Tabacundo, Ecuador",
    }
    productos_destacados = PRODUCTOS[:3]
    return render_template(
        "index.html",
        empresa=empresa,
        productos=productos_destacados,
        total_productos=len(PRODUCTOS),
    )


@app.route("/productos")
def productos():
    return render_template("productos.html", productos=PRODUCTOS, titulo_modulo="Catálogo de productos")


@app.route("/clientes")
def clientes():
    return render_template("clientes.html", clientes=CLIENTES, titulo_modulo="Nuestros clientes")


@app.route("/proveedores")
def proveedores():
    return render_template("proveedores.html", proveedores=PROVEEDORES, titulo_modulo="Proveedores")


@app.route("/facturacion")
def facturacion():
    total_facturado = sum(factura["total"] for factura in FACTURAS)
    return render_template(
        "facturacion.html",
        facturas=FACTURAS,
        total_facturado=total_facturado,
        titulo_modulo="Facturación",
    )


if __name__ == "__main__":
    app.run(debug=True)
