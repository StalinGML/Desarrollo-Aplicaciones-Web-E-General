from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp


class ProveedorForm(FlaskForm):

    empresa = StringField(
        "Nombre de la empresa",
        validators=[
            DataRequired(message="El nombre de la empresa es obligatorio."),
            Length(
                min=3,
                max=100,
                message="El nombre debe tener entre 3 y 100 caracteres."
            )
        ]
    )

    contacto = StringField(
        "Persona de contacto",
        validators=[
            DataRequired(message="El contacto es obligatorio."),
            Length(
                min=3,
                max=100,
                message="El contacto debe tener entre 3 y 100 caracteres."
            ),
            Regexp(
                r"^[A-Za-zÁÉÍÓÚáéíóúÑñÜü\s]+$",
                message="El contacto debe contener únicamente letras y espacios."
            )
        ]
    )

    correo = EmailField(
        "Correo electrónico",
        validators=[
            DataRequired(message="El correo es obligatorio."),
            Email(message="Ingrese un correo electrónico válido.")
        ]
    )

    telefono = StringField(
        "Teléfono",
        validators=[
            DataRequired(message="El teléfono es obligatorio."),
            Length(
                min=7,
                max=15,
                message="El teléfono debe tener entre 7 y 15 caracteres."
            ),
            Regexp(
                r"^\d+$",
                message="El teléfono debe contener únicamente números."
            )
        ]
    )

    submit = SubmitField("Registrar Proveedor")