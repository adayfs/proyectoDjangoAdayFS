from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse
from django.template import Template,Context
from django.template import loader
from reservas.models import Habitacion
from reservas.models import Reserva
from reservas.models import Cliente
import random
from random import randint



# Create your views here.
def reservas (request):
    plantilla=loader.get_template("index.html")
    todayNoFormat=datetime.today()
    today=todayNoFormat.strftime("%m/%d/%Y")
    numeroHabitaciones=Habitacion.objects.count()
    rooms = Reserva.objects.filter(fechaOut__gte=todayNoFormat)
    documento=plantilla.render({"reservas":rooms, "numHab":numeroHabitaciones, "numHabRes":(numeroHabitaciones- len(rooms)), "fecha":today})
    return HttpResponse(documento)

def buscador(request):
    return render(request, "buscador.html")


def resultadosBusqueda(request):
    plantilla=loader.get_template("resultados.html")   
    fechaIni=request.GET["fechaInicio"]
    fechaFin=request.GET["fechaFin"]
    personas=request.GET["personas"]
    todayNoFormat=datetime.today()
    today=todayNoFormat.strftime("%Y-%m-%d")
    if fechaIni<fechaFin and fechaIni>today:
        bien=True       
    else:
        bien=False
    
    dias=calcular_dias(fechaIni,fechaFin)
    habitacionesLibres=Habitacion.objects.filter(fechaOut__lte=fechaIni)
    habitaciones=[]
    for habitacion in habitacionesLibres:
        if habitacion.huespedes>=int(personas):
            habitaciones.append(habitacion)
    documento=plantilla.render({"exito":bien,"habLib":habitaciones, "numHab":len(habitaciones),"fechaIni":fechaIni, "fechaFin":fechaFin, "dias":dias})

    return HttpResponse(documento)

def reservar(request):
    plantilla=loader.get_template("reservar.html")

    elecciones=request.GET.getlist("eleccion")
    habitaciones=[]
    precioTotal=0
    fechaIni=request.GET["fechaIni"]
    fechaFin=request.GET["fechaFin"]
    dias=calcular_dias(fechaIni,fechaFin)

    for eleccion in elecciones:
        hab=Habitacion.objects.get(numeroHabitacion__exact=eleccion)
        habitaciones.append(hab)
        precioTotal+=hab.precio*dias

    documento=plantilla.render({"habitaciones":habitaciones, "precioTotal":precioTotal,"fechaIni":fechaIni, "fechaFin":fechaFin,"dias":dias})

    return HttpResponse(documento)

def calcular_dias(fechaIni, fechaFin):
    date_format = "%Y-%m-%d"
    a = datetime.strptime(fechaFin, date_format)
    b = datetime.strptime(fechaIni, date_format)
    delta = a - b
    dias=delta.days
    return dias 

def crear_reserva(request):
    plantilla=loader.get_template("exito.html")
    nuevo_cliente=request.GET.getlist("Contacto")
    obj, created = Cliente.objects.get_or_create(
        nombre=nuevo_cliente[0],
        apellidos=nuevo_cliente[1],
        email=nuevo_cliente[2],
        telefono=nuevo_cliente[3]
    )
   
    habitaciones=request.GET.getlist("habitacion")
    habitacionPrecio=request.GET.getlist("habitacionPrecio")
    habitacionH=request.GET.getlist("habitacionHuespedes")
    fechaIni=request.GET["fechaIni"]
    fechaFin=request.GET["fechaFin"]
    precio=request.GET["Precio"]
    localizador=""
    i=0
    for i in range(len(habitaciones)):
        if Reserva.objects.filter(numeroHabitacion=habitaciones[i]):
            exito=False       
        else:   
            ranNum = randint(100,999)
            localizador=str(ranNum)+random.choice(obj.nombre).upper()+random.choice(obj.nombre).upper()
            Reserva.objects.create(
                localizador=localizador,
                idCliente=obj.id,
                numeroHabitacion=habitaciones[i],
                fechaIn=fechaIni,
                fechaOut=fechaFin,
                numHuespedes=habitacionH[i],
                precio=habitacionPrecio[i],
                nombreCliente=obj.nombre,
                apellidosCliente=obj.apellidos        
            )
            exito=True
        Habitacion.objects.filter(numeroHabitacion=habitaciones[i]).update(fechaIn=fechaIni, fechaOut=fechaFin)
        
    todayNoFormat=datetime.today()
    today=todayNoFormat.strftime("%m/%d/%Y")
    numeroHabitaciones=Habitacion.objects.count()
    rooms = Reserva.objects.filter(fechaOut__gte=todayNoFormat)
    documento=plantilla.render({"localizador":localizador, "exito":exito})

    return HttpResponse(documento)
