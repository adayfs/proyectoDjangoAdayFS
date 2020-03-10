from django.http import HttpResponse
from django.template import Template,Context

def greetings(request):
    nombre="Aday"
    
    #Primero cargamos el fichero
    doc_externo=open("C:/Users/adayf/Desktop/Django/proyectoPrueba/proyectoPrueba/templates/templateD.html")
    #Luego lo leemos
    plt= Template(doc_externo.read())
    #Una vez cargado podemos cerrar el documento
    doc_externo.close()
    #Creamos el contexto,y añadimos un diccionario para añadirle valores que sustituiremos en la vista
    ctx=Context({"name":nombre})
    #Renderizamos
    documento=plt.render(ctx)

    return HttpResponse(documento)

