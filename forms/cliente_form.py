from flask_wtf import FlaskForm
from wtforms import StringField, EmailField
from wtforms.validators import DataRequired, Length, Email, Regexp


class ClienteForm(FlaskForm):

    nombre = StringField(
        "Nombre del cliente",
        validators=[
            DataRequired(message="El nombre es obligatorio."),
            Length(
                min=3,
                max=100,
                message="El nombre debe tener entre 3 y 100 caracteres."
            ),
            Regexp(
                r"^[A-Za-zÁÉÍÓÚáéíóúÑñÜü\s]+$",
                message="El nombre debe contener únicamente letras y espacios."
            )
        ]
    )

    cedula = StringField(
        "Cédula",
        validators=[
            DataRequired(message="La cédula es obligatoria."),
            Length(
                min=10,
                max=10,
                message="La cédula debe tener exactamente 10 dígitos."
            ),
            Regexp(
                r"^\d{10}$",
                message="La cédula debe contener únicamente 10 números."
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