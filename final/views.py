import json.decoder
import socket

import final.models
from final.models import *
from final.functions import veh_data, veh_update
from final import static_values
from final.forms import (Signup)

from datetime import datetime, timedelta

from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.views import View
from django.http import HttpResponse


def empty(request):
    return redirect('/login/')


def loginView(request, message=None):
    if request.method == 'GET':
        return render(request, 'login.html', message)
    elif request.method == 'POST':
        log = request.POST['log']
        pas = request.POST['pass']
        try:
            user = User.objects.get(login=log, password=pas)
            # set cookie
            expire_time = datetime.now() + timedelta(minutes=45)
            response = redirect('/home/')
            response.set_cookie('log', log, expires=expire_time)
            return response
        except final.models.User.DoesNotExist:
            return render(request, 'login.html', {'mess': 'No such user name or password, go to Sign up'})


def sign_up(request):
    if request.method == 'GET':
        form = Signup()
        return render(request, 'sign_up.html', {'form': form})
    elif request.method == 'POST':
        if 'Back' in request.POST:
            return redirect('/home/')
        form = Signup(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            username = data.get('username')
            email = data.get('email')
            company_name = data.get('company_name')
            password = data.get('password')
            user = User.objects.filter(login=username)
            if user:
                return render(request, 'sign_up.html', {'form': form, 'mess': 'Username already used'})
            user = User.objects.filter(email=email)
            if user:
                return render(request, 'sign_up.html', {'form': form, 'mess': 'Email already used'})
            else:
                User.objects.create(login=username,
                                    email=email,
                                    company_name=company_name,
                                    password=password)
                u = User.objects.get(login=username,
                                    email=email,
                                    company_name=company_name,
                                    password=password)
                Fleet.objects.create(user_id_id=u.id)
                return render(request, 'not_singed_in.html', static_values.Signed_up)
        else:
            errors = form.errors
            if 'username' in errors:
                return render(request, 'sign_up.html', {'form': form})
            elif 'email' in errors:
                return render(request, 'sign_up.html', {'form': form})
            elif 'password' in errors:
                return render(request, 'sign_up.html', {'form': form})


def home(request):
    log = request.COOKIES.get('log')
    if request.method == 'POST':
        response = redirect('/home/')
        response.delete_cookie('log')
        return response
    if not log:
        return render(request, 'not_singed_in.html', static_values.Not_signed_in)
    try:
        user = User.objects.get(login=log)
    except User.DoesNotExist:
        return redirect('')

    # save data into variables

    return render(request, 'home_page.html', {'user': user})


class Input_vehicle(View):

    def get(self, request):
        log = request.COOKIES.get('log')
        if not log:
            return render(request, 'not_singed_in.html', static_values.Not_signed_in)
        return render(request, 'input_vehicle.html')


    def post(self,request):
        log = request.COOKIES.get('log')
        if not log:
            return render(request, 'not_singed_in.html', static_values.Not_signed_in)
        user = User.objects.get(login=log)
        # save data into variables
        username = request.POST['username']
        password = request.POST['password']
        v_data, from_date = veh_data(username, password)
        for veh in v_data:
            vin = veh['Vin']
            try:
                V = Vehicle.objects.get(vin=vin)
                try:
                    F = Fleet.objects.get(user_id_id=user.id)
                    VehiclesInFleet.objects.get(Vehicle_id=V.id, Fleet_id=F.id)
                    # This is the refresh place
                    continue
                except VehiclesInFleet.DoesNotExist:
                    VehiclesInFleet.objects.create(Vehicle_id=V.id, Fleet_id=F.id)
                    F.amount += 1
                    F.save()
            except Vehicle.DoesNotExist:
                fuel_consumption = round(veh['EngineTotalFuelUsed'] / veh['HRTotalVehicleDistance'] * 100, 2)
                Vehicle.objects.create(avgFuelConsumptionPer100Km=fuel_consumption,
                                       vin=vin,
                                       last_data_upload=datetime.now(),
                                       first_data_upload=from_date,
                                       distance_traveled=veh['HRTotalVehicleDistance'],
                                       fuel_consumed=veh['EngineTotalFuelUsed'])
                V = Vehicle.objects.get(vin=vin)
                F = Fleet.objects.get(user_id_id=user.id)
                API.objects.create(username=username, password=password, vehicle_id=V.id)
                VehiclesInFleet.objects.create(Vehicle_id=V.id, Fleet_id=F.id)
                F.amount += 1
                F.save()
        return redirect('/home/')


class Show_Fleet(View):

    def get(self, request, error=''):
        log = request.COOKIES.get('log')
        if not log:
            return render(request, 'not_singed_in.html', static_values.Not_signed_in)
        user = User.objects.get(login=log)
        F = Fleet.objects.get(user_id_id=user.id)
        Veh = Vehicle.objects.filter(vehiclesinfleet__Fleet_id=F.id).order_by('avgFuelConsumptionPer100Km')
        paginator = Paginator(Veh, 15)  # Show 20 per page
        page = request.GET.get('page')
        vehicles = paginator.get_page(page)
        Fle_data = Fleet.objects.get(user_id_id=user.id)
        Fle_amount = Fle_data.amount

        data = {
            "user": user,
            "vehicle": vehicles,
            "fleet": Fle_amount,
            "error": error
        }
        return render(request, 'show_fleet.html', data)


    def post(self, request):
        for key in request.POST:
            if key.startswith("veh_"):
                veh_id = key.split("_")[1]
                V = Vehicle.objects.get(id=int(veh_id))
                try:
                    if V.last_data_upload.date() == datetime.now().date():
                        return Show_Fleet.get(self, request, "Vehicle is up to date")
                    if not veh_update(V):
                        fuel = 'something went wrong with API'
                        return HttpResponse(fuel)
                    else:
                        update_milage, update_fuel, fuel_consumption, time_update = veh_update(V)
                        V.distance_traveled += update_milage
                        V.fuel_consumed += update_fuel
                        V.last_data_upload = datetime.now()
                        V.average_fuel_consumption_from_update = fuel_consumption
                        V.days_from_update = time_update
                        fuel_consumption = round(V.fuel_consumed / V.distance_traveled * 100, 2)
                        V.avgFuelConsumptionPer100Km = fuel_consumption
                        V.save()
                        return Show_Fleet.get(self, request)
                except json.decoder.JSONDecodeError or socket.timeout:
                    return Show_Fleet.get(self, request, "Vehicles can be refreshed every 10s")


class Ranking(View):
    def get(self, request):
        log = request.COOKIES.get('log')
        if not log:
            return render(request, 'not_singed_in.html', static_values.Not_signed_in)
        user = User.objects.get(login=log)
        F = Fleet.objects.get(user_id_id=user.id)
        if F.amount == 0:
            return render(request, 'no_fleet.html')
        if user.company_name == '':
            return render(request, 'ranking_company_name.html')
        F = Fleet.objects.get(user_id_id=user.id)
        V_user = Vehicle.objects.filter(vehiclesinfleet__Fleet_id=F.id)
        Vin_user = [vehicle.vin for vehicle in V_user]
        Veh = Vehicle.objects.all().order_by('avgFuelConsumptionPer100Km')
        highest_position = None
        for i, vehicle in enumerate(Veh):
            if vehicle.vin in Vin_user:
                highest_position = i + 1
                break
        paginator = Paginator(Veh, 15)  # Show 20 per page
        page = request.GET.get('page')
        vehicles = paginator.get_page(page)
        data = {
            'position': highest_position,
            "user": user,
            'fleet': F.amount,
            'vins': Vin_user,
            "vehicle": vehicles,
        }
        return render(request, 'ranking.html', data)

    def post(self, request):
        log = request.COOKIES.get('log')
        if not log:
            return render(request, 'not_singed_in.html', static_values.Not_signed_in)
        user = User.objects.get(login=log)
        user.company_name = request.POST['company_name']
        user.save()
        return Ranking.get(self, request)