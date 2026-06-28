const formulario = document.getElementById("formSolicitud");
const nombreCliente = document.getElementById("nombreCliente");
const productoSolicitud = document.getElementById("productoSolicitud");
const tipoSolicitud = document.getElementById("tipoSolicitud");
const mensaje = document.getElementById("mensaje");
const listaSolicitudes = document.getElementById("listaSolicitudes");
const contador = document.getElementById("contador");

let totalSolicitudes = 0;

formulario.addEventListener("submit", function (event) {
    event.preventDefault();

    if (
        nombreCliente.value.trim() === "" ||
        productoSolicitud.value.trim() === "" ||
        tipoSolicitud.value === ""
    ) {
        mensaje.textContent = "Todos los campos son obligatorios.";
        mensaje.className = "text-danger mt-3 text-center fw-bold";
        return;
    }

    mensaje.textContent = "Solicitud registrada correctamente.";
    mensaje.className = "text-success mt-3 text-center fw-bold";

    const tarjeta = document.createElement("div");
    tarjeta.className = "card shadow p-3 mb-3";

    const contenido = document.createElement("p");
    contenido.innerHTML = `
        <strong>Cliente:</strong> ${nombreCliente.value}<br>
        <strong>Producto:</strong> ${productoSolicitud.value}<br>
        <strong>Categoría:</strong> ${tipoSolicitud.value}
    `;

    const botonEliminar = document.createElement("button");
    botonEliminar.textContent = "Eliminar";
    botonEliminar.className = "btn btn-danger btn-sm";

    botonEliminar.addEventListener("click", function () {
        tarjeta.remove();
        totalSolicitudes--;
        contador.textContent = totalSolicitudes;
    });

    tarjeta.appendChild(contenido);
    tarjeta.appendChild(botonEliminar);
    listaSolicitudes.appendChild(tarjeta);

    totalSolicitudes++;
    contador.textContent = totalSolicitudes;

    formulario.reset();
});