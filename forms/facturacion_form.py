from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DecimalField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange


class FacturacionForm(FlaskForm):

    cliente = StringField(
        "Cliente",
        validators=[
            DataRequired(message="El cliente es obligatorio."),
            Length(
                min=3,
                max=100,
                message="El cliente debe tener entre 3 y 100 caracteres."
            )
        ]
    )

    producto = StringField(
        "Producto",
        validators=[
            DataRequired(message="El producto es obligatorio."),
            Length(
                min=3,
                max=100,
                message="El producto debe tener entre 3 y 100 caracteres."
            )
        ]
    )

    cantidad = IntegerField(
        "Cantidad",
        validators=[
            DataRequired(message="La cantidad es obligatoria."),
            NumberRange(
                min=1,
                message="La cantidad debe ser mayor o igual a 1."
            )
        ]
    )

    precio = DecimalField(
        "Precio unitario",
        validators=[
            DataRequired(message="El precio es obligatorio."),
            NumberRange(
                min=0,
                message="El precio no puede ser negativo."
            )
        ],
        places=2
    )

    submit = SubmitField("Registrar Factura")