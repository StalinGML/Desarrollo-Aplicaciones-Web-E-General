from flask import Flask, render_template, request, redirect
from forms import (
    ProductoForm,
    ClienteForm,
    ProveedorForm,
    FacturacionForm
)

app = Flask(__name__)

# Clave secreta para Flask-WTF y protección CSRF
app.config["SECRET_KEY"] = "clave-secreta-proyecto"

solicitudes = []


# ==============================
# PÁGINA DE INICIO
# ==============================

@app.route("/")
def inicio():

    productos = [
        {
            "nombre": "Tubos",
            "descripcion": "Tubos de acero inoxidable de alta resistencia para aplicaciones industriales."
        },
        {
            "nombre": "Planchas",
            "descripcion": "Planchas resistentes para construcción y fabricación metálica."
        },
        {
            "nombre": "Perfiles",
            "descripcion": "Perfiles de acero inoxidable con gran resistencia estructural."
        },
        {
            "nombre": "Paneles Estampados",
            "descripcion": "Paneles con acabados decorativos y funcionales para distintos proyectos."
        },
        {
            "nombre": "Accesorios",
            "descripcion": "Accesorios y complementos en acero inoxidable de alta durabilidad."
        }
    ]

    return render_template(
        "index.html",
        productos=productos,
        solicitudes=solicitudes
    )


# ==============================
# PÁGINA DE PRODUCTOS
# ==============================

@app.route("/productos")
def productos():

    productos = [
        {
            "nombre": "Tubos",
            "imagen": "tubos.png",
            "descripcion": "Tubos de acero inoxidable para aplicaciones industriales, comerciales y de construcción.",
            "caracteristicas": [
                "Tipos: cuadrados, redondos y rectangulares.",
                "Medidas y espesores variables.",
                "Largo comercial de 6 metros."
            ]
        },
        {
            "nombre": "Planchas",
            "imagen": "planchas.png",
            "descripcion": "Planchas de acero inoxidable disponibles en diferentes calidades, espesores y acabados.",
            "caracteristicas": [
                "Medida estándar: 1220 × 2440 mm.",
                "Diferentes espesores.",
                "Disponibles en diferentes acabados."
            ]
        },
        {
            "nombre": "Perfiles",
            "imagen": "perfiles.png",
            "descripcion": "Perfiles de acero inoxidable utilizados en diferentes aplicaciones estructurales y de fabricación.",
            "caracteristicas": [
                "Tipos: barras, ángulos y platinas.",
                "Medidas y espesores variables.",
                "Largo comercial de 6 metros."
            ]
        },
        {
            "nombre": "Paneles Estampados",
            "imagen": "paneles.png",
            "descripcion": "Paneles de acero inoxidable con diferentes diseños y acabados decorativos.",
            "caracteristicas": [
                "Medida: 1 × 2 metros.",
                "Espesor: 0,9 mm.",
                "Modelos: punteados, lisos, texturizados y rugosos."
            ]
        },
        {
            "nombre": "Accesorios",
            "imagen": "accesorios.png",
            "descripcion": "Accesorios de acero inoxidable para diferentes aplicaciones de instalación y montaje.",
            "caracteristicas": [
                "Soportes.",
                "Codos y accesorios para tuberías.",
                "Manijas y accesorios para pasamanos."
            ]
        }
    ]

    return render_template(
        "productos.html",
        productos=productos
    )


# ==============================
# FORMULARIO DE PRODUCTOS
# ==============================

@app.route("/formulario-producto", methods=["GET", "POST"])
def formulario_producto():

    form = ProductoForm()

    if form.validate_on_submit():

        producto = {
            "nombre": form.nombre.data,
            "descripcion": form.descripcion.data
        }

        return render_template(
            "formulario_producto.html",
            form=form,
            producto=producto
        )

    return render_template(
        "formulario_producto.html",
        form=form
    )


# ==============================
# PÁGINA DE CLIENTES
# ==============================

@app.route("/clientes")
def clientes():

    clientes = [
        {
            "nombre": "Constructora Andina S.A.",
            "correo": "contacto@constructoraandina.com",
            "telefono": "0991234567"
        },
        {
            "nombre": "Metalúrgica del Pacífico",
            "correo": "ventas@metalurgicapacifico.com",
            "telefono": "0987654321"
        },
        {
            "nombre": "Industrias Guayaquil",
            "correo": "info@industriasguayaquil.com",
            "telefono": "0976543210"
        }
    ]

    return render_template(
        "clientes.html",
        clientes=clientes
    )


# ==============================
# FORMULARIO DE CLIENTES
# ==============================

@app.route("/formulario-cliente", methods=["GET", "POST"])
def formulario_cliente():

    form = ClienteForm()

    if form.validate_on_submit():

        cliente = {
            "nombre": form.nombre.data,
            "correo": form.correo.data,
            "telefono": form.telefono.data
        }

        return render_template(
            "formulario_cliente.html",
            form=form,
            cliente=cliente
        )

    return render_template(
        "formulario_cliente.html",
        form=form
    )


# ==============================
# PÁGINA DE PROVEEDORES
# ==============================

@app.route("/proveedores")
def proveedores():

    proveedores = [
        {
            "empresa": "Aceros del Ecuador S.A.",
            "contacto": "Carlos Mendoza",
            "correo": "ventas@acerosdelecuador.com",
            "telefono": "0991234567"
        },
        {
            "empresa": "Importadora Metalúrgica Cía. Ltda.",
            "contacto": "María González",
            "correo": "contacto@importadorametalurgica.com",
            "telefono": "0987654321"
        },
        {
            "empresa": "Distribuidora Nacional de Acero",
            "contacto": "Jorge Ramírez",
            "correo": "info@distribuidoranacional.com",
            "telefono": "0976543210"
        }
    ]

    return render_template(
        "proveedores.html",
        proveedores=proveedores
    )


# ==============================
# FORMULARIO DE PROVEEDORES
# ==============================

@app.route("/formulario-proveedor", methods=["GET", "POST"])
def formulario_proveedor():

    form = ProveedorForm()

    if form.validate_on_submit():

        proveedor = {
            "empresa": form.empresa.data,
            "contacto": form.contacto.data,
            "correo": form.correo.data,
            "telefono": form.telefono.data
        }

        return render_template(
            "formulario_proveedor.html",
            form=form,
            proveedor=proveedor
        )

    return render_template(
        "formulario_proveedor.html",
        form=form
    )


# ==============================
# PÁGINA DE FACTURACIÓN
# ==============================

@app.route("/facturacion")
def facturacion():

    facturas = [
        {
            "cliente": "Constructora Andina S.A.",
            "producto": "Tubos de acero inoxidable",
            "cantidad": 10,
            "precio": 45.50,
            "total": 455.00
        },
        {
            "cliente": "Metalúrgica del Pacífico",
            "producto": "Planchas de acero inoxidable",
            "cantidad": 5,
            "precio": 120.00,
            "total": 600.00
        },
        {
            "cliente": "Industrias Guayaquil",
            "producto": "Perfiles de acero inoxidable",
            "cantidad": 8,
            "precio": 35.75,
            "total": 286.00
        }
    ]

    return render_template(
        "facturacion.html",
        facturas=facturas
    )


# ==============================
# FORMULARIO DE FACTURACIÓN
# ==============================

@app.route("/formulario-facturacion", methods=["GET", "POST"])
def formulario_facturacion():

    form = FacturacionForm()

    if form.validate_on_submit():

        cantidad = form.cantidad.data
        precio = float(form.precio.data)
        total = cantidad * precio

        factura = {
            "cliente": form.cliente.data,
            "producto": form.producto.data,
            "cantidad": cantidad,
            "precio": precio,
            "total": total
        }

        return render_template(
            "formulario_facturacion.html",
            form=form,
            factura=factura
        )

    return render_template(
        "formulario_facturacion.html",
        form=form
    )


# ==============================
# REGISTRO DE COTIZACIONES
# ==============================

@app.route("/cotizar", methods=["POST"])
def cotizar():

    nombre = request.form.get("nombre", "").strip()
    producto = request.form.get("producto", "").strip()
    categoria = request.form.get("categoria", "").strip()

    if not nombre or not producto or not categoria:
        return "Todos los campos son obligatorios.", 400

    if len(nombre) < 3:
        return "El nombre debe tener mínimo 3 caracteres.", 400

    if len(producto) < 5:
        return "El producto debe contener más información.", 400

    if categoria not in ["Industrial", "Comercial", "Construcción"]:
        return "La categoría seleccionada no es válida.", 400

    solicitud = {
        "nombre": nombre,
        "producto": producto,
        "categoria": categoria
    }

    solicitudes.append(solicitud)

    return render_template(
        "cotizacion.html",
        nombre=nombre,
        producto=producto,
        categoria=categoria
    )


# ==============================
# ELIMINAR SOLICITUD
# ==============================

@app.route("/eliminar/<int:indice>", methods=["POST"])
def eliminar(indice):

    if 0 <= indice < len(solicitudes):
        solicitudes.pop(indice)

    return redirect("/")


# ==============================
# EJECUTAR APLICACIÓN
# ==============================

if __name__ == "__main__":
    app.run(debug=True)