from flask_wtf import FlaskForm
from wtforms import DecimalField, IntegerField, SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, NumberRange, Optional


class ProductoForm(FlaskForm):
    nombre = StringField("Nombre", validators=[DataRequired(), Length(min=3, max=120)])
    descripcion = TextAreaField("Descripción", validators=[DataRequired(), Length(min=10, max=500)])
    categoria = SelectField("Categoría", choices=[
        ("Papel floral", "Papel floral"), ("Empaques", "Empaques"), ("Cintas", "Cintas"),
        ("Bases", "Bases"), ("Mallas", "Mallas"), ("Accesorios", "Accesorios")],
        validators=[DataRequired()])
    precio = DecimalField("Precio", places=2, validators=[DataRequired(), NumberRange(min=0.01, max=99999)])
    stock = IntegerField("Stock", validators=[DataRequired(), NumberRange(min=0, max=999999)])
    imagen = StringField("Archivo de imagen", validators=[Optional(), Length(max=160)], default="producto_1.png")
    proveedor_id = SelectField("Proveedor", coerce=int, choices=[])
    submit = SubmitField("Guardar producto")
