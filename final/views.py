import json.decoder
import socket

import django.db.utils

import final.models
from final.models import *
from final.functions import veh_data, veh_update
from final import static_values
from final.forms import Signup, LoginForm, APIForm

from datetime import datetime, timedelta

from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.views import View
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


def empty(request):
    return redirect('/login/')


class LoginView(View):
    def get(self, request, message=''):
        context = {
            'mess': message,
            'form': LoginForm
        }
        return render(request, 'login.html', context)
    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            log = data.get('username')
            password = data.get('password')

            # uwierzytelnienie
            user = authenticate(
                username=log,
                password=password
            )
        if user:
            # logowanie
            login(request, user)
            return redirect('/home/')
        else:
            message = 'No such user name or password, go to Sign up'
            return LoginView.get(self, request, message=message)


class Sign_up(View):
    def get(self, request, message=''):
        form = Signup()
        return render(request, 'sign_up.html', {'form': form, 'mess': message})
    def post(self, request):
        if 'Back' in request.POST:
            return redirect('/home/')
        form = Signup(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            User.objects.create_user(
                username=data.get('login'),
                password=data.get('password'),
                first_name=data.get('first_name'),
                last_name=data.get('last_name'),
                email=data.get('email')
            )
            user = User.objects.get(username=data.get('login'))
            Fleet.objects.create(user_id=user)

            return redirect('/login/')
        else:
            return render(request, 'sign_up.html', {'form': form})


def home(request):
    if not request.user.is_authenticated:
        return render(request, 'not_singed_in.html', static_values.Not_signed_in)
    if request.method == 'POST':
        logout(request)
        return redirect('/login/')
    event = Event.objects.get(name='Refresh')

    # save data into variables

    return render(request, 'home.html', {'user': request.user, 'event': event})


class Input_vehicle(View):

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'not_singed_in.html', static_values.Not_signed_in)
        return render(request, 'input_vehicle.html', {'form': APIForm})


    def post(self,request):
        if not request.user.is_authenticated:
            return render(request, 'not_singed_in.html', static_values.Not_signed_in)
        if 'logout' in request.POST:
            logout(request)
            return redirect('/login/')
        # save data into variables
        form = APIForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            username = data.get('username')
            password = data.get('password')
            v_data, from_date = veh_data(username, password)
            user = request.user
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
        else:
            return render(request, 'input_vehicle.html', {'form': form})



class Show_Fleet(View):

    def get(self, request, error=''):
        if not request.user.is_authenticated:
            return render(request, 'not_singed_in.html', static_values.Not_signed_in)
        user = request.user
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
        if not request.user.is_authenticated:
            return render(request, 'not_singed_in.html', static_values.Not_signed_in)
        if 'logout' in request.POST:
            logout(request)
            return redirect('/login/')
        if 'back' in request.POST:
            return redirect('/home/')
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
        if not request.user.is_authenticated:
            return render(request, 'not_singed_in.html', static_values.Not_signed_in)
        user = request.user
        F = Fleet.objects.get(user_id_id=user.id)
        if F.amount == 0:
            return render(request, 'no_fleet.html')
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
        if not request.user.is_authenticated:
            return render(request, 'not_singed_in.html', static_values.Not_signed_in)
        if 'logout' in request.POST:
            logout(request)
            return redirect('/login/')
        user = request.user
        user.save()
        return Ranking.get(self, request)