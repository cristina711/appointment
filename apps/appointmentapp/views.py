# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import User, Appointment
from django.shortcuts import render, redirect
from django.contrib import messages
import datetime

# Create your views here.
def index(request):
    return render(request, 'appointmentapp/index.html')

def register(request):
    result = User.objects.validate_registration(request.POST)
    if type(result) == list:
        for err in result:
            messages.error(request, err)
        return redirect('/')
    request.session['user_id'] = result.id
    messages.success(request, "Successfully registered!")
    return redirect('/appointments')

def login(request):
    result = User.objects.validate_login(request.POST)
    if type(result) == list:
        for err in result:
            messages.error(request, err)
        return redirect('/')
    request.session['user_id'] = result.id
    messages.success(request, "Successfully logged in!")
    return redirect('/appointments')

def appointments(request):
    try:
        request.session['user_id']
    except KeyError:
        return redirect('/')
    user = User.objects.get(id=request.session['user_id'])
    appointments = Appointment.objects.filter(user_id=user.id)
    current_appointments = []
    future_appointments = []
    for appointment in appointments:
        if appointment.date == datetime.date.today():
            current_appointments.append(appointment)
        elif appointment.date > datetime.date.today():
            future_appointments.append(appointment)
    print current_appointments
    context = {
        'user': user,
        'today': datetime.date.today(),
        'current_appointments': current_appointments,
        'future_appointments': future_appointments,

    }
    return render(request, 'appointmentapp/appointments.html', context)

def edit_appointment(request, appointment_id):
    appointment = Appointment.objects.get(id=appointment_id)
    user = User.objects.get(id=request.session['user_id'])
    if appointment.user_id != user.id:
        messages.error(request, ["You are not allowed to edit this appointment"])
    context = {
        "user": user,
        "appointment": appointment,
    }
    return render(request, 'appointmentapp/edit_appointment.html', context)

def delete_appointment(request, appointment_id):
    appointment = Appointment.objects.get(id=appointment_id)
    user = User.objects.get(id=request.session['user_id'])
    if appointment.user_id != user.id:
        messages.error(request, ["You are not allowed to edit this appointment"])
    else:
        appointment.delete()
        return redirect('/appointments')

def update_appointment(request, appointment_id):
    appointment = Appointment.objects.get(id=appointment_id)
    user = User.objects.get(id=request.session['user_id'])
    if appointment.user_id != user.id:
        messages.error(request, ["You are not allowed to update this appointment"])
    else:
        Appointment.objects.create(user=user,
                                   tasks=request.POST['tasks'],
                                   date=request.POST['date'], 
                                   time=request.POST['time'],
                                   status=request.POST['status']
        )
        appointment.delete()
        return redirect('/appointments')

def add_appointment(request):
    user = User.objects.get(id=request.session['user_id'])
    Appointment.objects.create(user=user,
                                tasks=request.POST['tasks'],
                                date=request.POST['date'], 
                                time=request.POST['time'],
                                status=request.POST['status']
    )
    return redirect('/appointments')



    

    

# def logout
#     request.session.clear()
#     return redirect('/')