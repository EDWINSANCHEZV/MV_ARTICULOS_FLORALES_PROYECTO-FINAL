from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Regexp


class ClienteForm(FlaskForm):
    nombre = StringField("Nombre o empresa", validators=[DataRequired(), Length(min=3, max=120)])
    identificacion = StringField("Cédula o RUC", validators=[DataRequired(), Length(min=10, max=20),
                                  Regexp(r"^[0-9]+$", message="Ingrese solo números.")])
    telefono = StringField("Teléfono", validators=[DataRequired(), Length(min=7, max=30)])
    correo = StringField("Correo electrónico", validators=[DataRequired(), Email(), Length(max=120)])
    ciudad = StringField("Ciudad", validators=[DataRequired(), Length(min=2, max=80)])
    activo = BooleanField("Cliente activo", default=True)
    submit = SubmitField("Guardar cliente")
