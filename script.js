// =============================================================
// SEMANA 10 - CONTINUIDAD DEL FRONTEND PARA GITHUB PAGES
// Proyecto: MV Artículos Florales
// Se conserva el contenido dinámico y las validaciones anteriores.
// =============================================================

document.addEventListener("DOMContentLoaded", () => {
  // -----------------------------------------------------------
  // DATOS DINÁMICOS DE PRODUCTOS
  // -----------------------------------------------------------
  const productos = [
    {
      id: 1,
      nombre: "Papel Floral",
      descripcion: "Papeles decorativos para arreglos florales, empaques y presentación de rosas.",
      categoria: "Papel floral",
      imagen: "img/producto_1.png",
      estado: "Disponible"
    },
    {
      id: 2,
      nombre: "Malla Protectora",
      descripcion: "Material utilizado para proteger flores durante el cultivo, empaque y transporte.",
      categoria: "Mallas",
      imagen: "img/producto_2.png",
      estado: "Disponible"
    },
    {
      id: 3,
      nombre: "Fundas para Rosas",
      descripcion: "Fundas plásticas para proteger las flores y mejorar su presentación comercial.",
      categoria: "Empaques",
      imagen: "img/producto_3.png",
      estado: "Por consultar"
    }
  ];

  const bloquesPlantilla = [
    {
      titulo: "Encabezado y navegación",
      descripcion: "Contiene la identidad de la empresa y una navbar Bootstrap adaptable a computadora, tablet y celular.",
      icono: "1"
    },
    {
      titulo: "Contenido principal",
      descripcion: "Organiza la información en contenedores, filas, columnas, tarjetas y secciones reutilizables.",
      icono: "2"
    },
    {
      titulo: "Contenido dinámico",
      descripcion: "Renderiza productos y solicitudes desde arreglos de objetos mediante JavaScript y manipulación del DOM.",
      icono: "3"
    },
    {
      titulo: "Pie de página",
      descripcion: "Presenta los datos del proyecto, el autor y el año de elaboración de manera uniforme.",
      icono: "4"
    }
  ];

  // -----------------------------------------------------------
  // REFERENCIAS DEL DOM
  // -----------------------------------------------------------
  const contenedorProductos = document.getElementById("contenedorProductos");
  const spinnerProductos = document.getElementById("spinnerProductos");
  const resumenPlantillas = document.getElementById("resumenPlantillas");
  const alertaGlobal = document.getElementById("alertaGlobal");

  const formulario = document.getElementById("formSolicitud");
  const nombreProducto = document.getElementById("nombreProducto");
  const descripcionProducto = document.getElementById("descripcionProducto");
  const categoriaProducto = document.getElementById("categoriaProducto");
  const listaSolicitudes = document.getElementById("listaSolicitudes");
  const totalRegistros = document.getElementById("totalRegistros");
  const btnRegistrar = document.getElementById("btnRegistrar");
  const spinnerRegistro = document.getElementById("spinnerRegistro");
  const textoBtnRegistrar = document.getElementById("textoBtnRegistrar");

  const modalProductoElemento = document.getElementById("modalProducto");
  const modalEliminarElemento = document.getElementById("modalEliminar");
  const modalProducto = bootstrap.Modal.getOrCreateInstance(modalProductoElemento);
  const modalEliminar = bootstrap.Modal.getOrCreateInstance(modalEliminarElemento);

  let productoSeleccionado = null;
  let solicitudPendienteEliminar = null;
  let solicitudes = cargarSolicitudes();

  // -----------------------------------------------------------
  // ALERTAS BOOTSTRAP
  // -----------------------------------------------------------
  function mostrarAlerta(mensaje, tipo = "success") {
    const iconos = {
      success: "✓",
      danger: "!",
      warning: "⚠",
      info: "i"
    };

    alertaGlobal.innerHTML = `
      <div class="alert alert-${tipo} alert-dismissible fade show shadow-sm" role="alert">
        <strong>${iconos[tipo] || "i"}</strong> ${mensaje}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Cerrar"></button>
      </div>
    `;

    window.setTimeout(() => {
      const alerta = alertaGlobal.querySelector(".alert");
      if (alerta) {
        bootstrap.Alert.getOrCreateInstance(alerta).close();
      }
    }, 5000);
  }

  // -----------------------------------------------------------
  // RENDERIZADO DE PRODUCTOS CON CARDS BOOTSTRAP
  // -----------------------------------------------------------
  function mostrarProductos() {
    contenedorProductos.innerHTML = productos.map((producto) => {
      const claseEstado = producto.estado === "Disponible"
        ? "text-bg-success"
        : "text-bg-warning";

      return `
        <article class="col-12 col-md-6 col-lg-4">
          <div class="card product-card h-100 border-0 shadow-sm">
            <img src="${producto.imagen}" class="card-img-top" alt="${producto.nombre}">
            <div class="card-body p-4">
              <div class="d-flex justify-content-between align-items-start gap-2 mb-2">
                <h3 class="card-title h4 text-success mb-0">${producto.nombre}</h3>
                <span class="badge ${claseEstado}">${producto.estado}</span>
              </div>
              <p class="card-text text-muted">${producto.descripcion}</p>
              <p class="small mb-3"><strong>Categoría:</strong> ${producto.categoria}</p>
              <div class="d-grid gap-2 d-sm-flex">
                <button class="btn btn-outline-success flex-fill btn-detalle" type="button" data-id="${producto.id}">
                  Ver detalles
                </button>
                <button class="btn btn-success flex-fill btn-solicitar" type="button" data-id="${producto.id}">
                  Solicitar
                </button>
              </div>
            </div>
          </div>
        </article>
      `;
    }).join("");
  }

  function simularCargaProductos() {
    window.setTimeout(() => {
      mostrarProductos();
      spinnerProductos.classList.add("d-none");
      contenedorProductos.classList.remove("d-none");
    }, 900);
  }

  // -----------------------------------------------------------
  // BLOQUES DINÁMICOS CONSERVADOS DE SEMANA 7
  // -----------------------------------------------------------
  function mostrarBloquesPlantilla() {
    resumenPlantillas.innerHTML = bloquesPlantilla.map((bloque) => `
      <article class="col-12 col-md-6 col-lg-3">
        <div class="card block-card h-100 border-0 shadow-sm">
          <div class="card-body p-4">
            <div class="icon-circle mb-3">${bloque.icono}</div>
            <h3 class="h5 text-success">${bloque.titulo}</h3>
            <p class="text-muted mb-0">${bloque.descripcion}</p>
          </div>
        </div>
      </article>
    `).join("");
  }

  // -----------------------------------------------------------
  // MODAL DE DETALLE DEL PRODUCTO
  // -----------------------------------------------------------
  function abrirModalProducto(idProducto) {
    const producto = productos.find((item) => item.id === idProducto);
    if (!producto) return;

    productoSeleccionado = producto;

    document.getElementById("modalProductoTitulo").textContent = producto.nombre;
    const imagen = document.getElementById("modalProductoImagen");
    imagen.src = producto.imagen;
    imagen.alt = producto.nombre;
    document.getElementById("modalProductoDescripcion").textContent = producto.descripcion;
    document.getElementById("modalProductoCategoria").textContent = producto.categoria;

    const estado = document.getElementById("modalProductoEstado");
    estado.textContent = producto.estado;
    estado.className = producto.estado === "Disponible"
      ? "badge text-bg-success"
      : "badge text-bg-warning";

    modalProducto.show();
  }

  function prepararFormularioDesdeProducto(producto) {
    nombreProducto.value = producto.nombre;
    categoriaProducto.value = producto.categoria;
    descripcionProducto.value = `Solicito información y disponibilidad del producto ${producto.nombre}.`;

    validarNombre();
    validarDescripcion();
    validarCategoria();

    document.getElementById("solicitudes").scrollIntoView({ behavior: "smooth" });
    nombreProducto.focus({ preventScroll: true });
  }

  contenedorProductos.addEventListener("click", (evento) => {
    const botonDetalle = evento.target.closest(".btn-detalle");
    const botonSolicitar = evento.target.closest(".btn-solicitar");

    if (botonDetalle) {
      abrirModalProducto(Number(botonDetalle.dataset.id));
    }

    if (botonSolicitar) {
      const producto = productos.find((item) => item.id === Number(botonSolicitar.dataset.id));
      if (producto) prepararFormularioDesdeProducto(producto);
    }
  });

  document.getElementById("btnSolicitarDesdeModal").addEventListener("click", () => {
    if (!productoSeleccionado) return;
    modalProducto.hide();
    prepararFormularioDesdeProducto(productoSeleccionado);
  });

  // -----------------------------------------------------------
  // VALIDACIONES DINÁMICAS CONSERVADAS DE SEMANA 6
  // -----------------------------------------------------------
  function aplicarEstadoValidacion(campo, idError, mensaje, esValido) {
    const error = document.getElementById(idError);

    campo.classList.toggle("is-valid", esValido);
    campo.classList.toggle("is-invalid", !esValido);

    if (!esValido && mensaje) {
      error.textContent = mensaje;
    }

    return esValido;
  }

  function validarNombre() {
    const valor = nombreProducto.value.trim();

    if (valor === "") {
      return aplicarEstadoValidacion(nombreProducto, "errorNombre", "El nombre del producto es obligatorio.", false);
    }

    if (valor.length < 3) {
      return aplicarEstadoValidacion(nombreProducto, "errorNombre", "El nombre debe tener mínimo 3 caracteres.", false);
    }

    return aplicarEstadoValidacion(nombreProducto, "errorNombre", "", true);
  }

  function validarDescripcion() {
    const valor = descripcionProducto.value.trim();

    if (valor === "") {
      return aplicarEstadoValidacion(descripcionProducto, "errorDescripcion", "La descripción es obligatoria.", false);
    }

    if (valor.length < 10) {
      return aplicarEstadoValidacion(descripcionProducto, "errorDescripcion", "La descripción debe tener mínimo 10 caracteres.", false);
    }

    return aplicarEstadoValidacion(descripcionProducto, "errorDescripcion", "", true);
  }

  function validarCategoria() {
    const esValido = categoriaProducto.value !== "";
    return aplicarEstadoValidacion(categoriaProducto, "errorCategoria", "Seleccione una categoría antes de registrar.", esValido);
  }

  function validarFormulario() {
    const nombreValido = validarNombre();
    const descripcionValida = validarDescripcion();
    const categoriaValida = validarCategoria();

    return nombreValido && descripcionValida && categoriaValida;
  }

  // -----------------------------------------------------------
  // LOCALSTORAGE Y RENDERIZADO DE SOLICITUDES
  // -----------------------------------------------------------
  function cargarSolicitudes() {
    try {
      const datos = localStorage.getItem("mvSolicitudesSemana8");
      return datos ? JSON.parse(datos) : [];
    } catch (error) {
      console.warn("No fue posible recuperar las solicitudes guardadas.", error);
      return [];
    }
  }

  function guardarSolicitudes() {
    try {
      localStorage.setItem("mvSolicitudesSemana8", JSON.stringify(solicitudes));
    } catch (error) {
      console.warn("No fue posible guardar las solicitudes.", error);
    }
  }

  function mostrarSolicitudes() {
    totalRegistros.textContent = solicitudes.length;

    if (solicitudes.length === 0) {
      listaSolicitudes.innerHTML = `
        <tr>
          <td colspan="4" class="text-center text-muted py-4">
            Todavía no existen solicitudes registradas.
          </td>
        </tr>
      `;
      return;
    }

    listaSolicitudes.innerHTML = solicitudes.map((solicitud) => `
      <tr>
        <td>
          <strong>${solicitud.nombre}</strong>
          <div class="small text-muted">${solicitud.descripcion}</div>
          <div class="small text-muted">Fecha: ${solicitud.fecha}</div>
        </td>
        <td>${solicitud.categoria}</td>
        <td><span class="badge text-bg-warning">${solicitud.estado}</span></td>
        <td class="text-center">
          <button type="button" class="btn btn-danger btn-sm btn-eliminar" data-id="${solicitud.id}">
            Eliminar
          </button>
        </td>
      </tr>
    `).join("");
  }

  function limpiarValidaciones() {
    [nombreProducto, descripcionProducto, categoriaProducto].forEach((campo) => {
      campo.classList.remove("is-valid", "is-invalid");
    });
  }

  function cambiarEstadoBotonRegistro(cargando) {
    btnRegistrar.disabled = cargando;
    spinnerRegistro.classList.toggle("d-none", !cargando);
    textoBtnRegistrar.textContent = cargando ? "Procesando..." : "Registrar solicitud";
  }

  formulario.addEventListener("submit", (evento) => {
    evento.preventDefault();

    if (!validarFormulario()) {
      mostrarAlerta("Revise los campos marcados antes de registrar la solicitud.", "danger");
      return;
    }

    cambiarEstadoBotonRegistro(true);

    // Spinner Bootstrap para representar el procesamiento solicitado en la tarea.
    window.setTimeout(() => {
      const nuevaSolicitud = {
        id: Date.now(),
        nombre: nombreProducto.value.trim(),
        descripcion: descripcionProducto.value.trim(),
        categoria: categoriaProducto.value,
        fecha: new Date().toLocaleDateString("es-EC"),
        estado: "Pendiente de revisión"
      };

      solicitudes.push(nuevaSolicitud);
      guardarSolicitudes();
      mostrarSolicitudes();
      formulario.reset();
      limpiarValidaciones();
      cambiarEstadoBotonRegistro(false);
      mostrarAlerta("La solicitud fue registrada correctamente.", "success");
    }, 1000);
  });

  nombreProducto.addEventListener("input", validarNombre);
  nombreProducto.addEventListener("blur", validarNombre);
  descripcionProducto.addEventListener("input", validarDescripcion);
  descripcionProducto.addEventListener("blur", validarDescripcion);
  categoriaProducto.addEventListener("change", validarCategoria);
  categoriaProducto.addEventListener("blur", validarCategoria);

  // -----------------------------------------------------------
  // MODAL PARA CONFIRMAR ELIMINACIÓN
  // -----------------------------------------------------------
  listaSolicitudes.addEventListener("click", (evento) => {
    const boton = evento.target.closest(".btn-eliminar");
    if (!boton) return;

    solicitudPendienteEliminar = Number(boton.dataset.id);
    modalEliminar.show();
  });

  document.getElementById("btnConfirmarEliminar").addEventListener("click", () => {
    solicitudes = solicitudes.filter((solicitud) => solicitud.id !== solicitudPendienteEliminar);
    guardarSolicitudes();
    mostrarSolicitudes();
    modalEliminar.hide();
    mostrarAlerta("La solicitud fue eliminada correctamente.", "warning");
    solicitudPendienteEliminar = null;
  });

  // -----------------------------------------------------------
  // FORMULARIO DE CONTACTO
  // -----------------------------------------------------------
  document.getElementById("formContacto").addEventListener("submit", (evento) => {
    evento.preventDefault();

    if (!evento.currentTarget.checkValidity()) {
      evento.currentTarget.classList.add("was-validated");
      mostrarAlerta("Complete todos los datos del formulario de contacto.", "danger");
      return;
    }

    evento.currentTarget.reset();
    evento.currentTarget.classList.remove("was-validated");
    mostrarAlerta("Gracias por contactarnos. Su mensaje fue enviado correctamente.", "success");
  });

  // -----------------------------------------------------------
  // CERRAR NAVBAR EN CELULARES DESPUÉS DE SELECCIONAR UN ENLACE
  // -----------------------------------------------------------
  document.querySelectorAll("#navbarContenido .nav-link").forEach((enlace) => {
    enlace.addEventListener("click", () => {
      const menu = document.getElementById("navbarContenido");
      const instancia = bootstrap.Collapse.getInstance(menu);
      if (instancia) instancia.hide();
    });
  });

  // -----------------------------------------------------------
  // EJECUCIÓN PRINCIPAL
  // -----------------------------------------------------------
  mostrarBloquesPlantilla();
  mostrarSolicitudes();
  simularCargaProductos();
});
