from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length


class ProductoForm(FlaskForm):

    nombre = StringField(
        "Nombre del producto",
        validators=[
            DataRequired(message="El nombre es obligatorio."),
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
            DataRequired(message="La descripción es obligatoria."),
            Length(
                min=10,
                max=300,
                message="La descripción debe tener entre 10 y 300 caracteres."
            )
        ]
    )

    submit = SubmitField("Registrar Producto")
