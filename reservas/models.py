from django.db import models

# Create your models here.



class Habitacion(models.Model):
    numeroHabitacion=models.CharField(max_length=3)
    huespedes=models.IntegerField()
    precio=models.IntegerField()
    reservada=models.BooleanField()
    ocupada=models.BooleanField()
    fechaIn=models.DateField(null=True)
    fechaOut=models.DateField(null=True)
    tipo=models.CharField(max_length=15)

    
class Cliente(models.Model):
    nombre=models.CharField(max_length=30)
    apellidos=models.CharField(max_length=30)
    email=models.EmailField()
    telefono=models.IntegerField()

class Reserva(models.Model):
    localizador=models.CharField(max_length=10)
    idCliente=models.IntegerField()
    numeroHabitacion=models.CharField(max_length=3)
    fechaIn=models.DateField()
    fechaOut=models.DateField()
    numHuespedes=models.IntegerField()
    precio=models.IntegerField()
    nombreCliente=models.CharField(max_length=30)
    apellidosCliente=models.CharField(max_length=30)     

  