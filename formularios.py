from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import InputRequired, Length, EqualTo

class formularioLogin(FlaskForm):
    logusuario= StringField('Usuario', validators=[InputRequired(message='Este campo no puede estar vacío')])
    logclave= PasswordField('Contraseña', validators=[InputRequired(message='Este campo no puede estar vacío')])
    enviar = SubmitField('INICIAR SESIÓN')
    

class formularioRegistro(FlaskForm):
    regnombre = StringField('Nombre', validators=[InputRequired(message='Este campo no puede estar vacío'), Length(min=5,max=10, message = 'Este campo debe tener entre 5 y 10 caracteres')])
    regusuario = StringField('Usuario', validators=[InputRequired(message='Este campo no puede estar vacío'), Length(min=5,max=10, message = 'Este campo debe tener entre 5 y 10 caracteres')])
    regclave = PasswordField('Contraseña', validators=[InputRequired(message='Este campo no puede estar vacío'), Length(min=5,max=10, message = 'Este campo debe tener entre 5 y 10 caracteres')])
    regclave2 = PasswordField('Confirmar Contraseña', validators=[InputRequired(message='Este campo no puede estar vacío'),EqualTo('regclave', message='Contraseñas deben ser iguales')])
    registrarse = SubmitField('REGISTRATE')

class formeditar(FlaskForm):
    editnombre = StringField('Nombre', validators=[InputRequired(message='Este campo no puede estar vacío')])
    editusuario = StringField('Usuario', validators=[InputRequired(message='Este campo no puede estar vacío')])
    guardar = SubmitField('Guardar')

