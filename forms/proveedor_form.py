from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email, Length


class ProveedorForm(FlaskForm):
    empresa = StringField("Empresa", validators=[DataRequired(), Length(min=3, max=120)])
    contacto = StringField("Persona de contacto", validators=[DataRequired(), Length(min=3, max=120)])
    telefono = StringField("Teléfono", validators=[DataRequired(), Length(min=7, max=30)])
    correo = StringField("Correo electrónico", validators=[DataRequired(), Email(), Length(max=120)])
    ciudad = StringField("Ciudad", validators=[DataRequired(), Length(min=2, max=80)])
    submit = SubmitField("Guardar proveedor")
