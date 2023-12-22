#importar la conexion con la base de datos
from flask_app.config.mysqlconnection import connectToMySQL
#importacion de expresiones regulares
import re 
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') #Expresion regular de email
#encargado de mostrar errores / mensajes
from flask import flash

class User:

    def __init__(self, data):
        #data = {diccionario con toda la info de la instancia}
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls, form):
        query = "insert into users (first_name, last_name, email, password) values (%(first_name)s, %(last_name)s, %(email)s, %(password)s)"
        result = connectToMySQL('esquema_examen_final').query_db(query, form)
        return result

    @staticmethod
    def validate_user(form):
        is_valid = True
        if len(form['first_name']) < 2:
            flash('Nombre debe tener al menos 2 caracteres', 'register')
            is_valid = False
        if len(form['last_name']) < 2:
            flash('Apellido debe tener al menos 2 caracteres', 'register')
            is_valid = False
        if len(form['password']) < 6:
            flash('Contraseña debe tener al menos 6 caracteres', 'register')
            is_valid = False
        query = "select * from users where email = %(email)s"
        results = connectToMySQL('esquema_examen_final').query_db(query, form)
        if len(results) >= 1:
            flash('E-mail registrado previamente', 'register')
            is_valid = False
        if form['password'] != form['confirm']:
            flash('Contraseñas no coinciden', 'register')
            is_valid = False
        if not EMAIL_REGEX.match(form['email']):
            flash('E-mail invalido', 'register')
            is_valid = False
        return is_valid

    @classmethod
    def get_by_email(cls, form):
        query = "select * from users where email = %(email)s"
        result = connectToMySQL('esquema_examen_final').query_db(query, form)
        if len(result) < 1:#significa que lista esta vacia, no existe email en la base de datos
            return False
        else:
            user = cls(result[0])
            return user 

    @classmethod
    def get_by_id(cls, form):
        query = "select * from users where id = %(id)s"
        result = connectToMySQL('esquema_examen_final').query_db(query, form)
        user = cls(result[0])
        return user