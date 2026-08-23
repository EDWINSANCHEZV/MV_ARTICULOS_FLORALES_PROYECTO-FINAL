document.addEventListener("DOMContentLoaded", () => {
  const menu = document.getElementById("menuFlask");
  document.querySelectorAll("#menuFlask .nav-link").forEach((enlace) => {
    enlace.addEventListener("click", () => {
      const instancia = bootstrap.Collapse.getInstance(menu);
      if (instancia) instancia.hide();
    });
  });
});
