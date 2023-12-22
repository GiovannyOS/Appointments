from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from datetime import datetime

import re

class Appointment:
    def __init__(self, data):
        self.id = data['id']
        self.task = data['task']
        self.date = data['date']
        self.status = data['status']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

    @staticmethod
    def validate_appointment(form):
        is_valid=True
        if form['task'] == '':
            flash('Task no puede ser vacio','appointments')
            is_valid=False
        if form['date']=='':
            flash('Ingrese una fecha','appointments')
            is_valid=False
        else:
            fecha_examen=datetime.strptime(form['date'], '%Y-%m-%d')
            hoy=datetime.now()
            if hoy<fecha_examen:
                flash('La fecha no puede ser en el futuro', 'appointments')
                is_valid=False
        return is_valid
    @classmethod
    def save(cls, form):
        query="insert into appointments (task, date, status, user_id) values (%(task)s,%(date)s, %(status)s, %(user_id)s)"
        result=connectToMySQL('esquema_examen_final').query_db(query, form)
        return result

    @classmethod
    def get_all(cls):
        query="select *from appointments"
        results = connectToMySQL('esquema_examen_final').query_db(query)
        appointments = []
        for appointment in results:
            appointments.append(cls(appointment))

        return appointments

    @classmethod           
    def get_by_id(cls, form):
        query = "select * from appointments where id = %(id)s"
        result = connectToMySQL('esquema_examen_final').query_db(query, form)
        appointment = cls(result[0])
        return appointment

    @classmethod
    def update(cls, form):
        query = "update appointments set task=%(task)s, date=%(date)s, status=%(status)s where id=%(id)s"
        result = connectToMySQL('esquema_examen_final').query_db(query, form)
        return result

    @classmethod
    def delete(cls, form):
        query = "delete from appointments where id = %(id)s"
        result = connectToMySQL('esquema_examen_final').query_db(query, form)
        return result
    