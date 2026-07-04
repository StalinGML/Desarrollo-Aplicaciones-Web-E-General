const formulario = document.getElementById("formSolicitud");
const nombreCliente = document.getElementById("nombreCliente");
const productoSolicitud = document.getElementById("productoSolicitud");
const tipoSolicitud = document.getElementById("tipoSolicitud");

const errorNombre = document.getElementById("errorNombre");
const errorProducto = document.getElementById("errorProducto");
const errorCategoria = document.getElementById("errorCategoria");

const mensaje = document.getElementById("mensaje");
const listaSolicitudes = document.getElementById("listaSolicitudes");
const contador = document.getElementById("contador");

const regexNombre = /^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$/;

let totalSolicitudes = 0;

/* VALIDACIONES */

function validarNombre() {
    const valor = nombreCliente.value.trim();

    if (valor === "") {
        errorNombre.textContent = "El nombre es obligatorio.";
        errorNombre.className = "text-danger";
        nombreCliente.classList.add("is-invalid");
        nombreCliente.classList.remove("is-valid");
        return false;
    }

    if (!regexNombre.test(valor)) {
        errorNombre.textContent = "Solo se permiten letras y espacios.";
        errorNombre.className = "text-danger";
        nombreCliente.classList.add("is-invalid");
        nombreCliente.classList.remove("is-valid");
        return false;
    }

    if (valor.length < 3) {
        errorNombre.textContent = "Debe tener mínimo 3 caracteres.";
        errorNombre.className = "text-danger";
        nombreCliente.classList.add("is-invalid");
        nombreCliente.classList.remove("is-valid");
        return false;
    } 

    errorNombre.textContent = "Nombre válido.";
    errorNombre.className = "text-success";
    nombreCliente.classList.add("is-valid");
    nombreCliente.classList.remove("is-invalid");
    return true;
}

function validarProducto() {
    const valor = productoSolicitud.value.trim();

    if (valor === "") {
        errorProducto.textContent = "El producto es obligatorio.";
        errorProducto.className = "text-danger";
        productoSolicitud.classList.add("is-invalid");
        productoSolicitud.classList.remove("is-valid");
        return false;
    }

    if (valor.length < 5) {
        errorProducto.textContent = "Debe contener más información.";
        errorProducto.className = "text-danger";
        productoSolicitud.classList.add("is-invalid");
        productoSolicitud.classList.remove("is-valid");
        return false;
    }

    errorProducto.textContent = "Producto válido.";
    errorProducto.className = "text-success";
    productoSolicitud.classList.add("is-valid");
    productoSolicitud.classList.remove("is-invalid");
    return true;
}

function validarCategoria() {
    if (tipoSolicitud.value === "") {
        errorCategoria.textContent = "Seleccione una categoría.";
        errorCategoria.className = "text-danger";
        tipoSolicitud.classList.add("is-invalid");
        tipoSolicitud.classList.remove("is-valid");
        return false;
    }

    errorCategoria.textContent = "Categoría válida.";
    errorCategoria.className = "text-success";
    tipoSolicitud.classList.add("is-valid");
    tipoSolicitud.classList.remove("is-invalid");
    return true;
}

/* EVENTOS EN TIEMPO REAL */

nombreCliente.addEventListener("input", validarNombre);
nombreCliente.addEventListener("blur", validarNombre);

productoSolicitud.addEventListener("input", validarProducto);
productoSolicitud.addEventListener("blur", validarProducto);

tipoSolicitud.addEventListener("change", validarCategoria);
tipoSolicitud.addEventListener("blur", validarCategoria);

/* SUBMIT */

formulario.addEventListener("submit", function (event) {
    event.preventDefault();

    const nombreValido = validarNombre();
    const productoValido = validarProducto();
    const categoriaValida = validarCategoria();

    if (!nombreValido || !productoValido || !categoriaValida) {
        mensaje.className = "alert alert-danger mt-3";
        mensaje.textContent = "Corrija los errores antes de registrar.";
        return;
    }

    mensaje.className = "alert alert-success mt-3";
    mensaje.textContent = "Solicitud registrada con éxito.";

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

    nombreCliente.classList.remove("is-valid");
    productoSolicitud.classList.remove("is-valid");
    tipoSolicitud.classList.remove("is-valid");

    errorNombre.textContent = "";
    errorProducto.textContent = "";
    errorCategoria.textContent = "";
});