# Guía breve para la defensa

## Preparación

1. Ejecute `iniciar.bat` y abra `http://127.0.0.1:5000`.
2. Cree una cuenta y luego inicie sesión.
3. Mantenga abiertas las páginas **Panel**, **Productos**, **Clientes**, **Proveedores** y **Facturación**.

## Demostración sugerida (3 a 5 minutos)

1. Presente la página inicial y explique que el sistema administra artículos florales.
2. Muestre el registro y el inicio de sesión. Indique que la contraseña se almacena mediante hash y que las páginas internas están protegidas.
3. En **Proveedores**, cree un proveedor, edítelo y muestre el listado.
4. En **Productos**, cree un producto relacionado con ese proveedor y modifique su stock o precio.
5. En **Clientes**, cree un cliente y actualice uno de sus datos.
6. En **Facturación**, seleccione el cliente y el producto, registre una venta y compruebe que el stock disminuye.
7. Edite la factura, cambie la cantidad y verifique nuevamente el stock.
8. Elimine una factura y explique que el stock se restaura.
9. Cierre la sesión e intente abrir `/productos` para demostrar la protección de rutas.

## Puntos técnicos para explicar

- Flask gestiona las rutas y Jinja2 genera las páginas dinámicas.
- Flask-WTF valida formularios y añade protección CSRF.
- Flask-Login administra sesiones y rutas privadas.
- Werkzeug protege las contraseñas mediante hash.
- La base de datos contiene claves primarias y foráneas.
- Las consultas usan parámetros para evitar inyección SQL.
- El sistema implementa Crear, Leer, Actualizar y Eliminar en más de tres tablas relacionadas.
