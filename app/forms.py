from wtforms import Form, StringField, PasswordField, IntegerField, FloatField, TextAreaField, SelectField
from wtforms.validators import InputRequired, Length, NumberRange, Optional

class LoginForm(Form):
    nombre = StringField('Usuario', [InputRequired(), Length(min=1, max=64)])
    password = PasswordField('Contraseña', [InputRequired()])

class ProductForm(Form):
    nombre = StringField('Nombre', [InputRequired()])
    descripcion = TextAreaField('Descripción', [Optional()])
    cantidad = IntegerField('Cantidad', [InputRequired(), NumberRange(min=0)])
    precio = FloatField('Precio', [InputRequired(), NumberRange(min=0)])
    almacen_id = SelectField('Almacén', coerce=int)
