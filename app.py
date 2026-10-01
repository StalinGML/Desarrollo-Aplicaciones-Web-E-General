from flask import Flask, render_template, request, redirect, send_file, flash
import os
from io import BytesIO

from dotenv import load_dotenv
from flask_login import (
    LoginManager,
    login_user,
    login_required,
    current_user,
    logout_user
)

from werkzeug.security import generate_password_hash, check_password_hash
from models import Usuario

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image
)

from conexion.conexion import obtener_conexion

from forms import (
    ProductoForm,
    ClienteForm,
    ProveedorForm,
    FacturacionForm,
    UsuarioForm,
    LoginForm
)

load_dotenv()


app = Flask(__name__)

app.secret_key = os.getenv("SECRET_KEY")

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute(
        """
        SELECT id, usuario
        FROM usuarios
        WHERE id = %s
        """,
        (user_id,)
    )

    usuario = cursor.fetchone()

    cursor.close()
    conexion.close()

    if usuario is None:
        return None

    return Usuario(
        id=usuario[0],
        usuario=usuario[1]
    )

# ==============================
# CONFIGURACIÓN DE MYSQL
# ==============================

DATABASE = os.path.join("data", "ferreteria.db")


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
# REGISTRO DE USUARIOS
# ==============================

@app.route("/registro", methods=["GET", "POST"])
def registro():

    form = UsuarioForm()

    if form.validate_on_submit():

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute(
            """
            SELECT id
            FROM usuarios
            WHERE usuario = %s
            """,
            (form.usuario.data,)
        )

        usuario_existente = cursor.fetchone()

        if usuario_existente is not None:

            cursor.close()
            conexion.close()

            return render_template(
                "registro.html",
                form=form,
                error="El nombre de usuario ya está registrado."
            )

        password_hash = generate_password_hash(
            form.password.data
        )

        cursor.execute(
            """
            INSERT INTO usuarios (usuario, password)
            VALUES (%s, %s)
            """,
            (
                form.usuario.data,
                password_hash
            )
        )

        conexion.commit()

        cursor.close()
        conexion.close()

        return redirect("/login")

    return render_template(
        "registro.html",
        form=form
    )


# ==============================
# INICIO DE SESIÓN
# ==============================

@app.route("/login", methods=["GET", "POST"])
def login():

    form = LoginForm()

    if form.validate_on_submit():

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute(
            """
            SELECT id, usuario, password
            FROM usuarios
            WHERE usuario = %s
            """,
            (form.usuario.data,)
        )

        usuario_db = cursor.fetchone()

        cursor.close()
        conexion.close()

        if usuario_db is None:
            return render_template(
                "login.html",
                form=form,
                error="Usuario o contraseña incorrectos."
            )

        if not check_password_hash(
            usuario_db[2],
            form.password.data
        ):
            return render_template(
                "login.html",
                form=form,
                error="Usuario o contraseña incorrectos."
            )

        usuario = Usuario(
            id=usuario_db[0],
            usuario=usuario_db[1]
        )

        login_user(usuario)

        return redirect("/dashboard")

    return render_template(
        "login.html",
        form=form
    )

# ==============================
# DASHBOARD
# ==============================

@app.route("/dashboard")
@login_required
def dashboard():

    return render_template(
        "dashboard.html"
    )

# ==============================
# CERRAR SESIÓN
# ==============================

@app.route("/logout")
@login_required
def logout():

    logout_user()

    return redirect("/login")

# ==============================
# PÁGINA DE PRODUCTOS
# ==============================

@app.route("/productos")
@login_required
def productos():

    # Catálogo existente
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

    # Productos almacenados en la base de datos

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT
            p.id_producto,
            p.nombre,
            p.descripcion,
            p.precio,
            p.stock,
            pr.nombre
        FROM productos p
        LEFT JOIN proveedores pr
            ON p.id_proveedor = pr.id_proveedor
        ORDER BY p.id_producto DESC
    """)

    productos_db = cursor.fetchall()

    cursor.close()
    conexion.close()

    return render_template(
        "productos.html",
        productos=productos,
        productos_db=productos_db
    )


# ==============================
# FORMULARIO DE PRODUCTOS
# ==============================

@app.route("/formulario-producto", methods=["GET", "POST"])
@login_required
def formulario_producto():

    # Obtener proveedores registrados
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT
            id_proveedor,
            nombre
        FROM proveedores
        ORDER BY nombre
    """)

    proveedores_db = cursor.fetchall()

    cursor.close()
    conexion.close()

    # Crear formulario
    form = ProductoForm()

    # Cargar proveedores en el selector
    form.id_proveedor.choices = [
        (proveedor[0], proveedor[1])
        for proveedor in proveedores_db
    ]

    if form.validate_on_submit():

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute(
            """
            INSERT INTO productos
            (
                nombre,
                descripcion,
                precio,
                stock,
                id_proveedor
            )
            VALUES (%s, %s, %s, %s, %s)
            """,
            (
                form.nombre.data,
                form.descripcion.data,
                form.precio.data,
                form.stock.data,
                form.id_proveedor.data
            )
        )

        conexion.commit()

        cursor.close()
        conexion.close()

        return redirect("/productos")

    return render_template(
        "formulario_producto.html",
        form=form,
        editar=False
    )


# ==============================
# EDITAR PRODUCTO
# ==============================

@app.route("/editar-producto/<int:id>", methods=["GET", "POST"])
@login_required
def editar_producto(id):

    # Obtener proveedores
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT
            id_proveedor,
            nombre
        FROM proveedores
        ORDER BY nombre
    """)

    proveedores_db = cursor.fetchall()

    cursor.close()
    conexion.close()

    # Obtener producto
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute(
        """
        SELECT
            id_producto,
            nombre,
            descripcion,
            precio,
            stock,
            id_proveedor
        FROM productos
        WHERE id_producto = %s
        """,
        (id,)
    )

    producto = cursor.fetchone()

    cursor.close()
    conexion.close()

    if producto is None:
        return redirect("/productos")

    # Crear formulario
    form = ProductoForm()

    # Cargar proveedores en el selector
    form.id_proveedor.choices = [
        (proveedor[0], proveedor[1])
        for proveedor in proveedores_db
    ]

    # Cargar datos actuales del producto
    if request.method == "GET":

        form.nombre.data = producto[1]
        form.descripcion.data = producto[2]
        form.precio.data = producto[3]
        form.stock.data = producto[4]
        form.id_proveedor.data = producto[5]

    # Procesar actualización
    if form.validate_on_submit():

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute(
            """
            UPDATE productos
            SET
                nombre = %s,
                descripcion = %s,
                precio = %s,
                stock = %s,
                id_proveedor = %s
            WHERE id_producto = %s
            """,
            (
                form.nombre.data,
                form.descripcion.data,
                form.precio.data,
                form.stock.data,
                form.id_proveedor.data,
                id
            )
        )

        conexion.commit()

        cursor.close()
        conexion.close()

        return redirect("/productos")

    return render_template(
        "formulario_producto.html",
        form=form,
        editar=True
    )

# ==============================
# ELIMINAR PRODUCTO
# ==============================

@app.route("/eliminar-producto/<int:id>", methods=["POST"])
@login_required
def eliminar_producto(id):

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:

        cursor.execute(
            """
            DELETE FROM productos
            WHERE id_producto = %s
            """,
            (id,)
        )

        conexion.commit()

        flash(
            "Producto eliminado correctamente.",
            "success"
        )

    except Exception:

        conexion.rollback()

        flash(
            "No se puede eliminar este producto porque está asociado a una factura.",
            "danger"
        )

    finally:

        cursor.close()
        conexion.close()

    return redirect("/productos")

# ==============================
# PÁGINA DE CLIENTES
# ==============================

@app.route("/clientes")
@login_required
def clientes():

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT
            id_cliente,
            nombre,
            cedula,
            telefono,
            correo
        FROM clientes
        ORDER BY id_cliente DESC
    """)

    clientes_db = cursor.fetchall()

    cursor.close()
    conexion.close()

    return render_template(
        "clientes.html",
        clientes_db=clientes_db
    )


# ==============================
# AGREGAR CLIENTE
# ==============================

@app.route("/formulario-cliente", methods=["GET", "POST"])
@login_required
def formulario_cliente():

    form = ClienteForm()

    if form.validate_on_submit():

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute(
            """
            INSERT INTO clientes
            (nombre, cedula, telefono, correo)
            VALUES (%s, %s, %s, %s)
            """,
            (
                form.nombre.data,
                form.cedula.data,
                form.telefono.data,
                form.correo.data
            )
        )

        conexion.commit()

        cursor.close()
        conexion.close()

        return redirect("/clientes")

    return render_template(
        "formulario_cliente.html",
        form=form,
        editar=False
    )


# ==============================
# EDITAR CLIENTE
# ==============================

@app.route("/editar-cliente/<int:id>", methods=["GET", "POST"])
@login_required
def editar_cliente(id):

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute(
        """
        SELECT
            id_cliente,
            nombre,
            cedula,
            telefono,
            correo
        FROM clientes
        WHERE id_cliente = %s
        """,
        (id,)
    )

    cliente = cursor.fetchone()

    cursor.close()
    conexion.close()

    if cliente is None:
        return redirect("/clientes")

    form = ClienteForm()

    if request.method == "GET":

        form.nombre.data = cliente[1]
        form.cedula.data = cliente[2]
        form.telefono.data = cliente[3]
        form.correo.data = cliente[4]

    if form.validate_on_submit():

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute(
            """
            UPDATE clientes
            SET
                nombre = %s,
                cedula = %s,
                telefono = %s,
                correo = %s
            WHERE id_cliente = %s
            """,
            (
                form.nombre.data,
                form.cedula.data,
                form.telefono.data,
                form.correo.data,
                id
            )
        )

        conexion.commit()

        cursor.close()
        conexion.close()

        return redirect("/clientes")

    return render_template(
        "formulario_cliente.html",
        form=form,
        editar=True
    )

# ==============================
# ELIMINAR CLIENTE
# ==============================

@app.route("/eliminar-cliente/<int:id>", methods=["POST"])
@login_required
def eliminar_cliente(id):

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:

        cursor.execute(
            """
            DELETE FROM clientes
            WHERE id_cliente = %s
            """,
            (id,)
        )

        conexion.commit()

        flash(
            "Cliente eliminado correctamente.",
            "success"
        )

    except Exception:

        conexion.rollback()

        flash(
            "No se puede eliminar este cliente porque tiene facturas asociadas.",
            "danger"
        )

    finally:

        cursor.close()
        conexion.close()

    return redirect("/clientes")

# ==============================
# PÁGINA DE PROVEEDORES
# ==============================

@app.route("/proveedores")
@login_required
def proveedores():

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT
            id_proveedor,
            nombre,
            telefono,
            correo
        FROM proveedores
        ORDER BY id_proveedor DESC
    """)

    proveedores_db = cursor.fetchall()

    cursor.close()
    conexion.close()

    return render_template(
        "proveedores.html",
        proveedores_db=proveedores_db
    )


# ==============================
# AGREGAR PROVEEDOR
# ==============================

@app.route("/formulario-proveedor", methods=["GET", "POST"])
@login_required
def formulario_proveedor():

    form = ProveedorForm()

    if form.validate_on_submit():

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute(
            """
            INSERT INTO proveedores
            (nombre, telefono, correo)
            VALUES (%s, %s, %s)
            """,
            (
                form.nombre.data,
                form.telefono.data,
                form.correo.data
            )
        )

        conexion.commit()

        cursor.close()
        conexion.close()

        return redirect("/proveedores")

    return render_template(
        "formulario_proveedor.html",
        form=form,
        editar=False
    )


# ==============================
# EDITAR PROVEEDOR
# ==============================

@app.route("/editar-proveedor/<int:id>", methods=["GET", "POST"])
@login_required
def editar_proveedor(id):

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute(
        """
        SELECT
            id_proveedor,
            nombre,
            telefono,
            correo
        FROM proveedores
        WHERE id_proveedor = %s
        """,
        (id,)
    )

    proveedor = cursor.fetchone()

    cursor.close()
    conexion.close()

    if proveedor is None:
        return redirect("/proveedores")

    form = ProveedorForm()

    if request.method == "GET":

        form.nombre.data = proveedor[1]
        form.telefono.data = proveedor[2]
        form.correo.data = proveedor[3]

    if form.validate_on_submit():

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute(
            """
            UPDATE proveedores
            SET
                nombre = %s,
                telefono = %s,
                correo = %s
            WHERE id_proveedor = %s
            """,
            (
                form.nombre.data,
                form.telefono.data,
                form.correo.data,
                id
            )
        )

        conexion.commit()

        cursor.close()
        conexion.close()

        return redirect("/proveedores")

    return render_template(
        "formulario_proveedor.html",
        form=form,
        editar=True
    )


# ==============================
# ELIMINAR PROVEEDOR
# ==============================

@app.route("/eliminar-proveedor/<int:id>", methods=["POST"])
@login_required
def eliminar_proveedor(id):

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:

        cursor.execute(
            """
            DELETE FROM proveedores
            WHERE id_proveedor = %s
            """,
            (id,)
        )

        conexion.commit()

        flash(
            "Proveedor eliminado correctamente.",
            "success"
        )

    except Exception:

        conexion.rollback()

        flash(
            "No se puede eliminar este proveedor porque tiene productos asociados.",
            "danger"
        )

    finally:

        cursor.close()
        conexion.close()

    return redirect("/proveedores")

# ==============================
# PÁGINA DE FACTURACIÓN
# ==============================

@app.route("/facturacion")
@login_required
def facturacion():

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT
            f.id_factura,
            f.numero_factura,
            c.nombre,
            p.nombre,
            df.cantidad,
            df.precio,
            df.subtotal,
            f.fecha,
            f.total,
            f.estado
        FROM facturas f
        INNER JOIN clientes c
            ON f.id_cliente = c.id_cliente
        INNER JOIN detalle_factura df
            ON f.id_factura = df.id_factura
        INNER JOIN productos p
            ON df.id_producto = p.id_producto
        ORDER BY f.id_factura DESC
    """)

    facturas_db = cursor.fetchall()

    cursor.close()
    conexion.close()

    return render_template(
        "facturacion.html",
        facturas_db=facturas_db
    )

# ==============================
# FORMULARIO DE FACTURACIÓN
# ==============================

@app.route("/formulario-facturacion", methods=["GET", "POST"])
@login_required
def formulario_facturacion():

    # ==========================================
    # OBTENER CLIENTES
    # ==========================================

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT
            id_cliente,
            nombre
        FROM clientes
        ORDER BY nombre
    """)

    clientes_db = cursor.fetchall()

    cursor.close()
    conexion.close()


    # ==========================================
    # OBTENER PRODUCTOS
    # ==========================================

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT
            id_producto,
            nombre,
            precio,
            stock
        FROM productos
        ORDER BY nombre
    """)

    productos_db = cursor.fetchall()

    cursor.close()
    conexion.close()


    # ==========================================
    # CREAR FORMULARIO
    # ==========================================

    form = FacturacionForm()

    form.cliente.choices = [
        (cliente[0], cliente[1])
        for cliente in clientes_db
    ]

    form.producto.choices = [
        (producto[0], producto[1])
        for producto in productos_db
    ]


    # ==========================================
    # REGISTRAR FACTURA
    # ==========================================

    if form.validate_on_submit():

        id_cliente = form.cliente.data
        id_producto = form.producto.data
        cantidad = form.cantidad.data


        # ==========================================
        # OBTENER PRECIO Y STOCK DEL PRODUCTO
        # ==========================================

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute(
            """
            SELECT
                precio,
                stock,
                nombre
            FROM productos
            WHERE id_producto = %s
            """,
            (id_producto,)
        )

        producto = cursor.fetchone()

        cursor.close()
        conexion.close()


        # ==========================================
        # VERIFICAR PRODUCTO
        # ==========================================

        if producto is None:

            return render_template(
                "formulario_facturacion.html",
                form=form,
                productos_db=productos_db,
                error="El producto seleccionado no existe."
            )


        precio = producto[0]
        stock = producto[1]
        nombre_producto = producto[2]


        # ==========================================
        # VERIFICAR STOCK
        # ==========================================

        if cantidad > stock:

            return render_template(
                "formulario_facturacion.html",
                form=form,
                productos_db=productos_db,
                error=(
                    f"Stock insuficiente. "
                    f"Disponible: {stock} unidades."
                )
            )


        # ==========================================
        # CALCULAR TOTAL
        # ==========================================

        subtotal = precio * cantidad
        total = subtotal


        # ==========================================
        # GENERAR NÚMERO DE FACTURA
        # ==========================================

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute(
            """
            SELECT
                id_factura
            FROM facturas
            ORDER BY id_factura DESC
            LIMIT 1
            """
        )

        ultima_factura = cursor.fetchone()

        if ultima_factura is None:
            siguiente_numero = 1
        else:
            siguiente_numero = ultima_factura[0] + 1


        numero_factura = (
            f"FAC 001-001-{siguiente_numero:05d}"
        )


        # ==========================================
        # INSERTAR FACTURA
        # ==========================================

        cursor.execute(
            """
            INSERT INTO facturas
            (
                numero_factura,
                id_cliente,
                fecha,
                total
            )
            VALUES (%s, %s, CURRENT_DATE, %s)
            RETURNING id_factura
            """,
            (
                numero_factura,
                id_cliente,
                total
            )
        )

        id_factura = cursor.fetchone()[0]


        # ==========================================
        # INSERTAR DETALLE DE FACTURA
        # ==========================================

        cursor.execute(
            """
            INSERT INTO detalle_factura
            (
                id_factura,
                id_producto,
                cantidad,
                precio,
                subtotal
            )
            VALUES (%s, %s, %s, %s, %s)
            """,
            (
                id_factura,
                id_producto,
                cantidad,
                precio,
                subtotal
            )
        )


        # ==========================================
        # ACTUALIZAR STOCK
        # ==========================================

        cursor.execute(
            """
            UPDATE productos
            SET stock = stock - %s
            WHERE id_producto = %s
            """,
            (
                cantidad,
                id_producto
            )
        )


        # ==========================================
        # CONFIRMAR CAMBIOS
        # ==========================================

        conexion.commit()

        cursor.close()
        conexion.close()


        # ==========================================
        # OBTENER NOMBRE DEL CLIENTE
        # ==========================================

        cliente_nombre = next(
            (
                cliente[1]
                for cliente in clientes_db
                if cliente[0] == id_cliente
            ),
            "Cliente"
        )


        # ==========================================
        # DATOS DE LA FACTURA REGISTRADA
        # ==========================================

        factura = {
            "id_factura": id_factura,
            "numero_factura": numero_factura,
            "cliente": cliente_nombre,
            "producto": nombre_producto,
            "cantidad": cantidad,
            "precio": precio,
            "total": total
        }


        # ==========================================
        # MOSTRAR CONFIRMACIÓN
        # ==========================================

        return render_template(
            "formulario_facturacion.html",
            form=form,
            productos_db=productos_db,
            factura=factura
        )


    # ==========================================
    # MOSTRAR FORMULARIO
    # ==========================================

    return render_template(
        "formulario_facturacion.html",
        form=form,
        productos_db=productos_db
    )

# ==============================
# EDITAR FACTURA
# ==============================

@app.route("/editar-factura/<int:id>", methods=["GET", "POST"])
@login_required
def editar_factura(id):

    # ==========================================
    # OBTENER FACTURA
    # ==========================================

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute(
        """
        SELECT
            f.id_factura,
            f.id_cliente,
            df.id_producto,
            df.cantidad
        FROM facturas f
        INNER JOIN detalle_factura df
            ON f.id_factura = df.id_factura
        WHERE f.id_factura = %s
          AND f.estado = 'ACTIVA'
        """,
        (id,)
    )

    factura = cursor.fetchone()

    cursor.close()
    conexion.close()


    # ==========================================
    # VERIFICAR FACTURA
    # ==========================================

    if factura is None:
        return "Factura no encontrada o anulada", 404


    id_factura = factura[0]
    id_cliente_actual = factura[1]
    id_producto_actual = factura[2]
    cantidad_actual = factura[3]


    # ==========================================
    # OBTENER CLIENTES
    # ==========================================

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute(
        """
        SELECT
            id_cliente,
            nombre
        FROM clientes
        ORDER BY nombre
        """
    )

    clientes_db = cursor.fetchall()

    cursor.close()
    conexion.close()


    # ==========================================
    # OBTENER PRODUCTOS
    # ==========================================

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute(
        """
        SELECT
            id_producto,
            nombre,
            precio,
            stock
        FROM productos
        ORDER BY nombre
        """
    )

    productos_db = cursor.fetchall()

    cursor.close()
    conexion.close()


    # ==========================================
    # CREAR FORMULARIO
    # ==========================================

    form = FacturacionForm()

    form.cliente.choices = [
        (cliente[0], cliente[1])
        for cliente in clientes_db
    ]

    form.producto.choices = [
        (producto[0], producto[1])
        for producto in productos_db
    ]


    # ==========================================
    # CARGAR DATOS ACTUALES
    # ==========================================

    if request.method == "GET":

        form.cliente.data = id_cliente_actual
        form.producto.data = id_producto_actual
        form.cantidad.data = cantidad_actual


    # ==========================================
    # PROCESAR EDICIÓN
    # ==========================================

    if form.validate_on_submit():

        nuevo_cliente = form.cliente.data
        nuevo_producto = form.producto.data
        nueva_cantidad = form.cantidad.data


        # ==========================================
        # INICIAR CONEXIÓN
        # ==========================================

        conexion = obtener_conexion()
        cursor = conexion.cursor()


        try:

            # ==========================================
            # DEVOLVER STOCK DE LA FACTURA ORIGINAL
            # ==========================================

            cursor.execute(
                """
                UPDATE productos
                SET stock = stock + %s
                WHERE id_producto = %s
                """,
                (
                    cantidad_actual,
                    id_producto_actual
                )
            )


            # ==========================================
            # OBTENER PRECIO Y STOCK DEL NUEVO PRODUCTO
            # ==========================================

            cursor.execute(
                """
                SELECT
                    precio,
                    stock,
                    nombre
                FROM productos
                WHERE id_producto = %s
                """,
                (nuevo_producto,)
            )

            producto = cursor.fetchone()


            if producto is None:

                conexion.rollback()

                cursor.close()
                conexion.close()

                return render_template(
                    "editar_factura.html",
                    form=form,
                    factura=factura,
                    error="El producto seleccionado no existe."
                )


            nuevo_precio = producto[0]
            stock_disponible = producto[1]


            # ==========================================
            # VERIFICAR STOCK
            # ==========================================

            if nueva_cantidad > stock_disponible:

                conexion.rollback()

                cursor.close()
                conexion.close()

                return render_template(
                    "editar_factura.html",
                    form=form,
                    factura=factura,
                    error=(
                        f"Stock insuficiente. "
                        f"Disponible: {stock_disponible} unidades."
                    )
                )


            # ==========================================
            # CALCULAR NUEVO TOTAL
            # ==========================================

            nuevo_subtotal = nuevo_precio * nueva_cantidad
            nuevo_total = nuevo_subtotal


            # ==========================================
            # ACTUALIZAR FACTURA
            # ==========================================

            cursor.execute(
                """
                UPDATE facturas
                SET
                    id_cliente = %s,
                    total = %s
                WHERE id_factura = %s
                """,
                (
                    nuevo_cliente,
                    nuevo_total,
                    id_factura
                )
            )


            # ==========================================
            # ACTUALIZAR DETALLE
            # ==========================================

            cursor.execute(
                """
                UPDATE detalle_factura
                SET
                    id_producto = %s,
                    cantidad = %s,
                    precio = %s,
                    subtotal = %s
                WHERE id_factura = %s
                """,
                (
                    nuevo_producto,
                    nueva_cantidad,
                    nuevo_precio,
                    nuevo_subtotal,
                    id_factura
                )
            )


            # ==========================================
            # DESCONTAR NUEVO STOCK
            # ==========================================

            cursor.execute(
                """
                UPDATE productos
                SET stock = stock - %s
                WHERE id_producto = %s
                """,
                (
                    nueva_cantidad,
                    nuevo_producto
                )
            )


            # ==========================================
            # CONFIRMAR CAMBIOS
            # ==========================================

            conexion.commit()


        except Exception:

            conexion.rollback()

            cursor.close()
            conexion.close()

            return "Ocurrió un error al actualizar la factura.", 500


        cursor.close()
        conexion.close()


        return redirect("/facturacion")


    # ==========================================
    # MOSTRAR FORMULARIO
    # ==========================================

    return render_template(
        "editar_factura.html",
        form=form,
        factura=factura
    )

# ==============================
# ANULAR FACTURA
# ==============================

@app.route("/anular-factura/<int:id>", methods=["POST"])
@login_required
def anular_factura(id):

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:

        # ==========================================
        # OBTENER PRODUCTO Y CANTIDAD DE LA FACTURA
        # ==========================================

        cursor.execute(
            """
            SELECT
                df.id_producto,
                df.cantidad
            FROM detalle_factura df
            INNER JOIN facturas f
                ON df.id_factura = f.id_factura
            WHERE df.id_factura = %s
              AND f.estado = 'ACTIVA'
            """,
            (id,)
        )

        detalle = cursor.fetchone()


        # ==========================================
        # VERIFICAR FACTURA
        # ==========================================

        if detalle is None:

            cursor.close()
            conexion.close()

            return "Factura no encontrada o ya está anulada.", 404


        id_producto = detalle[0]
        cantidad = detalle[1]


        # ==========================================
        # DEVOLVER STOCK
        # ==========================================

        cursor.execute(
            """
            UPDATE productos
            SET stock = stock + %s
            WHERE id_producto = %s
            """,
            (
                cantidad,
                id_producto
            )
        )


        # ==========================================
        # CAMBIAR ESTADO DE LA FACTURA
        # ==========================================

        cursor.execute(
            """
            UPDATE facturas
            SET estado = 'ANULADA'
            WHERE id_factura = %s
              AND estado = 'ACTIVA'
            """,
            (id,)
        )


        # ==========================================
        # CONFIRMAR CAMBIOS
        # ==========================================

        conexion.commit()


    except Exception:

        conexion.rollback()

        cursor.close()
        conexion.close()

        return "Ocurrió un error al anular la factura.", 500


    cursor.close()
    conexion.close()


    return redirect("/facturacion")


# ==============================
# DESCARGAR FACTURA EN PDF
# ==============================

@app.route("/descargar-factura/<int:id>")
@login_required
def descargar_factura(id):

    # ==========================================
    # OBTENER DATOS DE LA FACTURA
    # ==========================================

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute(
        """
        SELECT
            f.numero_factura,
            f.fecha,
            c.nombre,
            c.cedula,
            c.correo,
            c.telefono,
            p.nombre,
            df.cantidad,
            df.precio,
            df.subtotal,
            f.total
        FROM facturas f
        INNER JOIN clientes c
            ON f.id_cliente = c.id_cliente
        INNER JOIN detalle_factura df
            ON f.id_factura = df.id_factura
        INNER JOIN productos p
            ON df.id_producto = p.id_producto
        WHERE f.id_factura = %s
        """,
        (id,)
    )

    factura = cursor.fetchone()

    cursor.close()
    conexion.close()


    # ==========================================
    # VERIFICAR FACTURA
    # ==========================================

    if factura is None:

        return "Factura no encontrada", 404


    (
        numero_factura,
        fecha,
        cliente,
        cedula,
        correo,
        telefono,
        producto,
        cantidad,
        precio,
        subtotal,
        total
    ) = factura


    # ==========================================
    # CREAR PDF EN MEMORIA
    # ==========================================

    pdf_buffer = BytesIO()

    documento = SimpleDocTemplate(
        pdf_buffer,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )


    estilos = getSampleStyleSheet()

    estilo_titulo = estilos["Title"]
    estilo_titulo.alignment = TA_CENTER

    estilo_normal = estilos["Normal"]


    contenido = []


    # ==========================================
    # ENCABEZADO
    # ==========================================

    ruta_logo = os.path.join(
        app.root_path,
        "static",
        "img",
        "logo.png"
    )

    logo = Image(
        ruta_logo,
        width=80,
        height=60
    )

    contenido.append(logo)

    contenido.append(
        Spacer(1, 8)
    )

    contenido.append(
        Paragraph(
            "IMPORDYCOM S.A.",
            estilo_titulo
        )
    )

    contenido.append(
        Paragraph(
            "Importadora y Distribuidora de Materiales",
            estilo_normal
        )
    )

    contenido.append(
        Spacer(1, 15)
    )


    # ==========================================
    # INFORMACIÓN DE LA FACTURA
    # ==========================================

    informacion_factura = [
        ["N.º Factura", numero_factura],
        ["Fecha", str(fecha)],
    ]

    tabla_factura = Table(
        informacion_factura,
        colWidths=[120, 350]
    )

    tabla_factura.setStyle(
        TableStyle([
            (
                "BACKGROUND",
                (0, 0),
                (0, -1),
                colors.lightgrey
            ),
            (
                "FONTNAME",
                (0, 0),
                (0, -1),
                "Helvetica-Bold"
            ),
            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.5,
                colors.grey
            ),
            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "MIDDLE"
            ),
        ])
    )

    contenido.append(tabla_factura)

    contenido.append(
        Spacer(1, 15)
    )


    # ==========================================
    # DATOS DEL CLIENTE
    # ==========================================

    contenido.append(
        Paragraph(
            "<b>Datos del cliente</b>",
            estilos["Heading3"]
        )
    )

    datos_cliente = [
        ["Cliente", cliente],
        ["Cédula", cedula],
        ["Correo", correo],
        ["Teléfono", telefono],
    ]

    tabla_cliente = Table(
        datos_cliente,
        colWidths=[120, 350]
    )

    tabla_cliente.setStyle(
        TableStyle([
            (
                "BACKGROUND",
                (0, 0),
                (0, -1),
                colors.lightgrey
            ),
            (
                "FONTNAME",
                (0, 0),
                (0, -1),
                "Helvetica-Bold"
            ),
            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.5,
                colors.grey
            ),
        ])
    )

    contenido.append(tabla_cliente)

    contenido.append(
        Spacer(1, 20)
    )


    # ==========================================
    # DETALLE DE PRODUCTO
    # ==========================================

    contenido.append(
        Paragraph(
            "<b>Detalle de la factura</b>",
            estilos["Heading3"]
        )
    )

    detalle = [
        [
            "Producto",
            "Cantidad",
            "Precio unitario",
            "Subtotal"
        ],
        [
            producto,
            str(cantidad),
            f"${float(precio):.2f}",
            f"${float(subtotal):.2f}"
        ]
    ]

    tabla_detalle = Table(
        detalle,
        colWidths=[190, 70, 110, 100]
    )

    tabla_detalle.setStyle(
        TableStyle([
            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                colors.darkgrey
            ),
            (
                "TEXTCOLOR",
                (0, 0),
                (-1, 0),
                colors.white
            ),
            (
                "FONTNAME",
                (0, 0),
                (-1, 0),
                "Helvetica-Bold"
            ),
            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.5,
                colors.grey
            ),
            (
                "ALIGN",
                (1, 1),
                (-1, -1),
                "CENTER"
            ),
        ])
    )

    contenido.append(tabla_detalle)

    contenido.append(
        Spacer(1, 20)
    )


    # ==========================================
    # TOTAL
    # ==========================================

    tabla_total = Table(
        [
            [
                "TOTAL",
                f"${float(total):.2f}"
            ]
        ],
        colWidths=[370, 100]
    )

    tabla_total.setStyle(
        TableStyle([
            (
                "BACKGROUND",
                (0, 0),
                (0, 0),
                colors.lightgrey
            ),
            (
                "FONTNAME",
                (0, 0),
                (-1, -1),
                "Helvetica-Bold"
            ),
            (
                "ALIGN",
                (1, 0),
                (1, 0),
                "RIGHT"
            ),
            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.5,
                colors.grey
            ),
        ])
    )

    contenido.append(tabla_total)

    contenido.append(
        Spacer(1, 30)
    )


    # ==========================================
    # MENSAJE FINAL
    # ==========================================

    contenido.append(
        Paragraph(
            "Gracias por su preferencia.",
            estilo_normal
        )
    )


    # ==========================================
    # GENERAR PDF
    # ==========================================

    documento.build(contenido)

    pdf_buffer.seek(0)


    # ==========================================
    # DESCARGAR PDF
    # ==========================================

    nombre_archivo = (
        numero_factura
        .replace(" ", "_")
        + ".pdf"
    )

    return send_file(
        pdf_buffer,
        as_attachment=True,
        download_name=nombre_archivo,
        mimetype="application/pdf"
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