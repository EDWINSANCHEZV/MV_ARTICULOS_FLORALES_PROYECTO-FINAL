from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Regexp


class LoginForm(FlaskForm):
    usuario = StringField("Usuario", validators=[DataRequired(), Length(min=4, max=50)])
    password = PasswordField("Contraseña", validators=[DataRequired(), Length(min=6, max=128)])
    recordarme = BooleanField("Recordar sesión")
    submit = SubmitField("Iniciar sesión")


class RegistroForm(FlaskForm):
    nombre = StringField("Nombre completo", validators=[DataRequired(), Length(min=3, max=120)])
    usuario = StringField("Usuario", validators=[DataRequired(), Length(min=4, max=50),
                          Regexp(r"^[A-Za-z0-9_.]+$", message="Use letras, números, punto o guion bajo.")])
    correo = StringField("Correo electrónico", validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField("Contraseña", validators=[DataRequired(), Length(min=8, max=128)])
    confirmar = PasswordField("Confirmar contraseña", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Crear cuenta")
