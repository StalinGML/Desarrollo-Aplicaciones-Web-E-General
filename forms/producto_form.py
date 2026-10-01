from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    TextAreaField,
    DecimalField,
    IntegerField,
    SelectField
)
from wtforms.validators import (
    DataRequired,
    Length,
    NumberRange
)


class ProductoForm(FlaskForm):

    nombre = StringField(
        "Nombre del producto",
        validators=[
            DataRequired(
                message="El nombre es obligatorio."
            ),
            Length(
                min=3,
                max=100,
                message="El nombre debe tener entre 3 y 100 caracteres."
            )
        ]
    )

    descripcion = TextAreaField(
        "Descripción",
        validators=[
            DataRequired(
                message="La descripción es obligatoria."
            ),
            Length(
                min=10,
                max=300,
                message="La descripción debe tener entre 10 y 300 caracteres."
            )
        ]
    )

    precio = DecimalField(
        "Precio",
        places=2,
        validators=[
            DataRequired(
                message="El precio es obligatorio."
            ),
            NumberRange(
                min=0,
                message="El precio no puede ser negativo."
            )
        ]
    )

    stock = IntegerField(
        "Stock",
        validators=[
            DataRequired(
                message="El stock es obligatorio."
            ),
            NumberRange(
                min=0,
                message="El stock debe ser un número entero igual o mayor que 0."
            )
        ]
    )

    id_proveedor = SelectField(
        "Proveedor",
        coerce=int,
        validators=[
            DataRequired(
                message="Debe seleccionar un proveedor."
            )
        ]
    )