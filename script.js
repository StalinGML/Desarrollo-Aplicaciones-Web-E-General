/* DATOS DINÁMICOS 
   Preparado para integrar con Flask */

const productos = [
    {
        nombre: "Tubos",
        descripcion: "Tubos de acero inoxidable de alta resistencia para aplicaciones industriales."
    },
    {
        nombre: "Planchas",
        descripcion: "Planchas resistentes para construcción y fabricación metálica."
    },
    {
        nombre: "Perfiles",
        descripcion: "Perfiles de acero inoxidable con gran resistencia estructural."
    },
    {
        nombre: "Paneles Estampados",
        descripcion: "Paneles con acabados decorativos y funcionales para distintos proyectos."
    },
    {
        nombre: "Accesorios",
        descripcion: "Accesorios y complementos en acero inoxidable de alta durabilidad."
    }
];

const contenedorProductos = document.getElementById("contenedorProductos");
const mensajeProductos = document.getElementById("mensajeProductos");

function mostrarProductos() {

    contenedorProductos.innerHTML = "";

    if (productos.length === 0) {

        mensajeProductos.innerHTML = `
            <div class="alert alert-warning">
                No existen productos registrados.
            </div>
        `;

        return;
    }

    mensajeProductos.innerHTML = "";

    productos.forEach(function(producto){

        const columna = document.createElement("div");
        columna.className = "col-md-4 mb-3";

        columna.innerHTML = `
            <div class="card h-100 shadow">

                <div class="card-body">

                    <h5 class="card-title">${producto.nombre}</h5>

                    <p class="card-text">
                        ${producto.descripcion}
                    </p>

                </div>

            </div>
        `;

        contenedorProductos.appendChild(columna);

    });

}

mostrarProductos();

/* FORMULARIO */

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
const spinnerCarga = document.getElementById("spinnerCarga");

const regexNombre = /^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$/;

let totalSolicitudes = 0;

/* VALIDACIÓN NOMBRE */

function validarNombre() {

    const valor = nombreCliente.value.trim();

    if (valor === "") {

        errorNombre.textContent = "El nombre es obligatorio.";
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

    if (!regexNombre.test(valor)) {

        errorNombre.textContent = "Solo se permiten letras y espacios.";
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

/* VALIDACIÓN PRODUCTO */

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

/* VALIDACIÓN CATEGORÍA */

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

/* ASIGNACIÓN DE EVENTOS */

nombreCliente.addEventListener("input", validarNombre);
nombreCliente.addEventListener("blur", validarNombre);

productoSolicitud.addEventListener("input", validarProducto);
productoSolicitud.addEventListener("blur", validarProducto);

tipoSolicitud.addEventListener("change", validarCategoria);
tipoSolicitud.addEventListener("blur", validarCategoria);

/* REGISTRO DE SOLICITUD */

formulario.addEventListener("submit", function(event){

    event.preventDefault();

    const nombreValido = validarNombre();
    const productoValido = validarProducto();
    const categoriaValida = validarCategoria();

    if (!nombreValido || !productoValido || !categoriaValida){

        mensaje.className = "alert alert-danger mt-3";
        mensaje.textContent = "Corrija los errores antes de registrar.";

        return;

    }

    spinnerCarga.classList.remove("d-none");
    mensaje.innerHTML = "";
    setTimeout(function () {
        spinnerCarga.classList.add("d-none");

        mensaje.className = "alert alert-success mt-3";
        mensaje.textContent = "Solicitud registrada con éxito.";

        const tarjeta = document.createElement("div");

        tarjeta.className = "card shadow p-3 mb-3";
        tarjeta.innerHTML = `

            <p>
                <strong>Cliente:</strong> ${nombreCliente.value}<br>
                <strong>Producto:</strong> ${productoSolicitud.value}<br>
                <strong>Categoría:</strong> ${tipoSolicitud.value}
            </p>
        `;
        const botonEliminar = document.createElement("button");

        botonEliminar.textContent = "Eliminar";
        botonEliminar.className = "btn btn-danger btn-sm";
        botonEliminar.addEventListener("click", function () {
            tarjeta.remove();

            totalSolicitudes--;
            contador.textContent = totalSolicitudes;

        });

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

    }, 1500);

});
