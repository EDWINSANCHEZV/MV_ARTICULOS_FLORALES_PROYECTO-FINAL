from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired, NumberRange


class FacturaForm(FlaskForm):
    cliente_id = SelectField("Cliente", coerce=int, choices=[], validators=[DataRequired()])
    producto_id = SelectField("Producto", coerce=int, choices=[], validators=[DataRequired()])
    cantidad = IntegerField("Cantidad", validators=[DataRequired(), NumberRange(min=1, max=9999)])
    estado = SelectField("Estado", choices=[("Pendiente", "Pendiente"), ("Pagada", "Pagada"),
                          ("Anulada", "Anulada")], validators=[DataRequired()])
    submit = SubmitField("Guardar factura")
