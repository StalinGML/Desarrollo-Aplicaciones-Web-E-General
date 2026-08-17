from flask import Flask, render_template, request, redirect

app = Flask(__name__)

solicitudes = []


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


@app.route("/productos")
def productos():

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
        "productos.html",
        productos=productos
    )


@app.route("/clientes")
def clientes():
    return render_template("clientes.html")


@app.route("/proveedores")
def proveedores():
    return render_template("proveedores.html")


@app.route("/facturacion")
def facturacion():
    return render_template("facturacion.html")


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


@app.route("/eliminar/<int:indice>", methods=["POST"])
def eliminar(indice):

    if 0 <= indice < len(solicitudes):
        solicitudes.pop(indice)

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)