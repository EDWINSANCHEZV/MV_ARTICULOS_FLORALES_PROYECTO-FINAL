from flask_wtf import FlaskForm
from wtforms import SubmitField


class EliminarForm(FlaskForm):
    submit = SubmitField("Confirmar")
