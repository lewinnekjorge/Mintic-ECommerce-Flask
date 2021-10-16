from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import InputRequired, Length, EqualTo

class formularioLogin(FlaskForm):
    logusuario= StringField('Usuario', validators=[InputRequired(message='Campo no puede estar vacío')])
    logclave= PasswordField('Contraseña', validators=[InputRequired(message='Campo no puede estar vacío')])
    enviar = SubmitField('INICIAR SESIÓN')
    

class formularioRegistro(FlaskForm):
    regnombre = StringField('Nombre', validators=[InputRequired(message='Campo no puede estar vacío')])
    regusuario = StringField('Usuario', validators=[InputRequired(message='Campo no puede estar vacío')])
    regclave = PasswordField('Contraseña', validators=[InputRequired(message='Campo no puede estar vacío')])
    regclave2 = PasswordField('Confirmar Contraseña', validators=[InputRequired(message='Campo no puede estar vacío'),EqualTo('regclave', message='Contraseñas deben ser iguales')])
    registrarse = SubmitField('REGISTRATE')

