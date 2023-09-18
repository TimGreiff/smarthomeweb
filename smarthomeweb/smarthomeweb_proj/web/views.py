from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required   
from .decorators import login_required_custom
from .models import Sensor, Werte
from web.forms.TempsFilterForm import TempsFilterForm
from web.forms.lfFilterForm import lfFilterForm
from web.forms.ldFilterForm import ldFilterForm
from web.forms.SensorEditModelForm import SensorEditModelForm
from django.db.models import Max, Min
from datetime import datetime, timedelta
from django.views.generic import TemplateView
from django.views.generic import View
from django.contrib.auth.views import LoginView
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.utils.decorators import method_decorator


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/web')  # Redirect to a success page
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html')



@method_decorator(login_required, name='dispatch')
class htmlviewer(TemplateView):
        template_name = "-placeholder-"


@method_decorator(login_required, name='dispatch')
class SensorListView(View):
    def get(self, request):
        queryset = Sensor.objects.all()
        return render(request, "web/sensors.html", {"sensorlist": list(queryset)})

        
 
@login_required
def tempdetails(request, temp_id):
    print(temp_id + "tempdetails")
    queryset = Sensor.objects.get(pk=temp_id)
    return HttpResponse(f"Tempdetails for Sensor-ID {temp_id}: {queryset.sen_raum}, {queryset.sen_ip}")


@login_required
def luftfeuchtedetails(request, luftfeuchte_id):
    print(luftfeuchte_id + "luftfeuchtedetails")
    queryset = Sensor.objects.get(pk=luftfeuchte_id)
    return HttpResponse(f"Luchtfeuchtigkeitsdetails for Sensor-ID {luftfeuchte_id}: {queryset.sen_raum}, {queryset.sen_ip}")


@login_required
def luftdruckdetails(request, luftdruck_id):
    print(luftdruck_id + "luftdruckdetails")
    queryset = Sensor.objects.get(pk=luftdruck_id)
    return HttpResponse(f"Luchtdruckdetails for Sensor-ID {luftdruck_id}: {queryset.sen_raum}, {queryset.sen_ip}")


@login_required
def edit_sensor_details(request, sensor_id):
    sensor = Sensor.objects.get(pk=sensor_id)

    if request.method == "POST":
        print("GET")
        form = SensorEditModelForm(request.POST, instance=sensor)
        if form.is_valid():
            form.save()
            return redirect("/web/sensors/")
    else:
        print("GET")
        print(sensor_id)
        form = SensorEditModelForm(instance=sensor)
        print(sensor)
        return render(request, "web/sensor_edit.html", {"form": form})
    
@login_required
def display_temps(request):
    print("display_temps")
    if request.method == "POST":
        form = TempsFilterForm(request.POST)
        print("display_temps")
        print(form)

        if form.is_valid():
            print(form.cleaned_data)
            lowerVal = form.cleaned_data["lowerVal"]
            if lowerVal is None:
                lowerVal = Werte.objects.aggregate(Min('temperatur'))["temperatur__min"]
                print(lowerVal)
            
            upperVal = form.cleaned_data["upperVal"]
            if upperVal is None:
                upperVal = Werte.objects.aggregate(Max('temperatur'))["temperatur__max"]
                print(upperVal)
                        
            # if upperVal is None:
                # upperVal = Werte.ob
            vonDate = form.cleaned_data["vonDate"]
            bisDate = form.cleaned_data["bisDate"]
            print(f"{lowerVal}, {upperVal}, {vonDate}, {bisDate}")
            # queryset = Werte.objects.filter(temperatur__lte = form.cleaned_data["upperVal"])
            # queryset = Werte.objects.filter(temperatur__range = (lowerVal, upperVal))
            queryset = Werte.objects.filter(datum__gte = vonDate, datum__lte = (bisDate + timedelta(days=1)),
                                            temperatur__lte = upperVal, temperatur__gte = lowerVal)
            
            
            return render(request, "web/temps.html", {"name": "Berg", "tempslist": list(queryset), "form": form})
        else:
            return HttpResponse(f"Error! {form.errors}")
    else:
        print("GET")
        form = TempsFilterForm()
        form.lowerVal = 4
        queryset = Werte.objects.all()
        return render(request, "web/temps.html", {"form": form, "tempslist": list(queryset)})
        

@login_required
def display_lf(request):
    print("display_lf")
    if request.method == "POST":
        form = lfFilterForm(request.POST)
        print("display_lf")
        print(form)

        if form.is_valid():
            print(form.cleaned_data)
            lowerVal = form.cleaned_data["lowerVal"]
            if lowerVal is None:
                lowerVal = Werte.objects.aggregate(Min('luftfeuchte'))["luftfeuchte__min"]
                print(lowerVal)
            
            upperVal = form.cleaned_data["upperVal"]
            if upperVal is None:
                upperVal = Werte.objects.aggregate(Max('luftfeuchte'))["luftfeuchte__max"]
                print(upperVal)
                        
            # if upperVal is None:
                # upperVal = Werte.ob
            vonDate = form.cleaned_data["vonDate"]
            bisDate = form.cleaned_data["bisDate"]
            print(f"{lowerVal}, {upperVal}, {vonDate}, {bisDate}")
            # queryset = Werte.objects.filter(temperatur__lte = form.cleaned_data["upperVal"])
            # queryset = Werte.objects.filter(temperatur__range = (lowerVal, upperVal))
            queryset = Werte.objects.filter(datum__gte = vonDate, datum__lte = (bisDate + timedelta(days=1)),
                                            luftfeuchte__lte = upperVal, luftfeuchte__gte = lowerVal)
            
            
            return render(request, "web/showhumid.html", {"name": "Berg", "lflist": list(queryset), "form": form})
        else:
            return HttpResponse(f"Error! {form.errors}")
    else:
        print("GET")
        form = ldFilterForm()
        form.lowerVal = 4
        queryset = Werte.objects.all()
        return render(request, "web/showhumid.html", {"form": form, "lflist": list(queryset)})
        

@login_required    
def display_ld(request):
    print("display_ld")
    if request.method == "POST":
        form = ldFilterForm(request.POST)
        print("display_ld")
        print(form)

        if form.is_valid():
            print(form.cleaned_data)
            lowerVal = form.cleaned_data["lowerVal"]
            if lowerVal is None:
                lowerVal = Werte.objects.aggregate(Min('luftdruck'))["luftdruck__min"]
                print(lowerVal)
            
            upperVal = form.cleaned_data["upperVal"]
            if upperVal is None:
                upperVal = Werte.objects.aggregate(Max('luftdruck'))["luftdruck__max"]
                print(upperVal)
                        
            # if upperVal is None:
                # upperVal = Werte.ob
            vonDate = form.cleaned_data["vonDate"]
            bisDate = form.cleaned_data["bisDate"]
            print(f"{lowerVal}, {upperVal}, {vonDate}, {bisDate}")
            # queryset = Werte.objects.filter(temperatur__lte = form.cleaned_data["upperVal"])
            # queryset = Werte.objects.filter(temperatur__range = (lowerVal, upperVal))
            queryset = Werte.objects.filter(datum__gte = vonDate, datum__lte = (bisDate + timedelta(days=1)),
                                            luftdruck__lte = upperVal, luftdruck__gte = lowerVal)
            
            
            return render(request, "web/showpress.html", {"name": "Berg", "ldlist": list(queryset), "form": form})
        else:
            return HttpResponse(f"Error! {form.errors}")
    else:
        print("GET")
        form = ldFilterForm()
        form.lowerVal = 4
        queryset = Werte.objects.all()
        return render(request, "web/showpress.html", {"form": form, "ldlist": list(queryset)})
        


@login_required
def add_sensor(request):
    if request.method == 'POST':
        # Retrieve data from the form
        sen_raum = request.POST['sensor_raum']
        sen_ip = request.POST['sensor_ip']
        sen_code = request.POST['sensor_code']

        # Create a new Sensor object and save it to the database
        sensor = Sensor(
            sen_raum=sen_raum,
            sen_ip=sen_ip,
            sen_code=sen_code,
        )
        sensor.save()

        # Redirect to a success page or display a success message
        return render(request, 'web/add_sensor_success.html')  # Replace 'success' with the actual URL or view name for success

    return render(request, 'web/newsensor.html')  
