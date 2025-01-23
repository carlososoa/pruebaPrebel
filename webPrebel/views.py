from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
from django.db import models
from webPrebel.models import Facturas

# Create your views here.

def guardarEnSqlServer():
    print('hola')


def punto1(request):

    return render(request, 'punto1.html')
    

def punto3(request):

    df = pd.read_excel('webPrebel\BASE_DATOS_FACTURAS.xlsx')
    
    #manejando los NaN
    df['numero_factura'].fillna('No especificado', inplace=True)  
    df['fecha_compra'].fillna(pd.Timestamp('today'), inplace=True)  


    for _, row in df.iterrows():
        Facturas.objects.create(

            codigo_producto = row['codigo_producto'],
            nombre_producto = row['nombre_producto'],
            cantidad = row['cantidad'],
            fecha_compra = row['fecha_compra'],
            numero_factura = row['numero_factura']

    )
        
    facturas = Facturas.objects.all()

    context = {
        'facturas': facturas
    }   
    
    



    return render(request, 'punto3.html', context)
    
