document.addEventListener("DOMContentLoaded", () => {
  const menu = document.getElementById("menuFlask");
  document.querySelectorAll("#menuFlask .nav-link").forEach((enlace) => {
    enlace.addEventListener("click", () => {
      const instancia = bootstrap.Collapse.getInstance(menu);
      if (instancia) instancia.hide();
    });
  });

  document.querySelectorAll(".form-eliminar").forEach((formulario) => {
    formulario.addEventListener("submit", (evento) => {
      if (!window.confirm("¿Está seguro de eliminar este registro?")) evento.preventDefault();
    });
  });
});
