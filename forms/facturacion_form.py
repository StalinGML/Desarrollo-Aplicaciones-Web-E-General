from flask_wtf import FlaskForm
from wtforms import SelectField, IntegerField
from wtforms.validators import DataRequired, NumberRange


class FacturacionForm(FlaskForm):

    cliente = SelectField(
        "Cliente",
        coerce=int,
        validators=[
            DataRequired(
                message="Debe seleccionar un cliente."
            )
        ]
    )

    producto = SelectField(
        "Producto",
        coerce=int,
        validators=[
            DataRequired(
                message="Debe seleccionar un producto."
            )
        ]
    )

    cantidad = IntegerField(
        "Cantidad",
        validators=[
            DataRequired(
                message="La cantidad es obligatoria."
            ),
            NumberRange(
                min=1,
                message="La cantidad debe ser mayor o igual a 1."
            )
        ]
    )