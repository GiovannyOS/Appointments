from flask import Flask, render_template, redirect, session, request, flash
from flask_app import app

from flask_app.models.users import User
from flask_app.models.appointments import Appointment

@app.route('/new/appointment')
def new_appointment():
    if 'user_id' not in session:
        flash('Favor de iniciar sesión', 'not_in_session')
        return redirect('/')
    return render_template('new.html')

@app.route('/create/appointment', methods=['POST'])
def create_appointment():
    if 'user_id' not in session:
        flash('Favor de iniciar sesión', 'not_in_session')
        return redirect('/')
    if not Appointment.validate_appointment(request.form):
        return redirect('/new/appointment')
    Appointment.save(request.form)
    return redirect('/dashboard')

@app.route('/edit/appointment/<int:id>')
def edit_appointment(id):
    if 'user_id' not in session:
        flash('Favor de iniciar sesión', 'not_in_session')
        return redirect('/')
    #buscar la instancia de Grade que corresponde al id
    diccionario = {"id":id}
    appointment = Appointment.get_by_id(diccionario)
    return render_template('edit.html', appointment=appointment)

@app.route('/update/appointment', methods=['POST'])
def update_appointment():
    if 'user_id' not in session:
        flash('Favor de iniciar sesión', 'not_in_session')
        return redirect('/')
    #valida que el formulario sea correcto
    if not Appointment.validate_appointment(request.form):
        return redirect('/edit/appointment/'+request.form['id'])

    Appointment.update(request.form)
    return redirect('/dashboard')

@app.route('/delete/appointment/<int:id>')
def delete_appointment(id):
    if 'user_id' not in session:
        flash('Favor de iniciar sesión', 'not_in_session')
        return redirect('/')
    #BORRAR
    form = {"id":id}
    Appointment.delete(form)
    return redirect('/dashboard')