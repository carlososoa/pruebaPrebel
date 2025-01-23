from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
from django.db import models
from webPrebel.models import Facturas
import PyPDF2
import openpyxl as op

# Create your views here.

def guardarEnSqlServer():
    print('hola')


def logicapunto1():
    import PyPDF2
    import pandas as pd
    import openpyxl as op

    pdf_file_obj =  open ('webPrebel/3. FAC001.pdf', 'rb')
    pdf_read = PyPDF2.PdfReader(pdf_file_obj)

    pdf_file_obj2 =  open ('webPrebel/4. FAC002.pdf', 'rb')
    pdf_read2 = PyPDF2.PdfReader(pdf_file_obj2)

    page_obj = pdf_read.pages[0]
    page_obj2 = pdf_read2.pages[0]

    text = page_obj.extract_text()
    text2 = page_obj2.extract_text()

    lineas = text.split('\n')
    lineas2 = text2.split('\n')
    #lineas.append(lineas2[2:])

    df = pd.DataFrame([linea.split() for linea in lineas if linea.strip()])
    headers = lineas[2].split()
    headers.append('numero_factura')
    headers.append('fecha_compra')
    #print(headers)
    processed_data = []
    for linea in lineas[3:]:
        partes = [None] * 5
        sec = linea.split()
        partes[0] = sec[0]
        partes[1] = ''
        facturaNumber = lineas[0].split()[1]
        fecha = lineas[1].split()[1]
        print(fecha)
        print(facturaNumber)
        
        for i in   sec[1: (len(sec) -1)]:
            partes[1] = str(partes[1])+ str(' ') + str(i)
        partes[2] = sec[len(sec)-1]
        
        partes[3] = facturaNumber
        partes[4] = fecha

        processed_data.append(partes)

    processed_data2 = []
    for linea in lineas2[3:]:
        partes = [None] * 5
        sec = linea.split()
        partes[0] = sec[0]
        partes[1] = ''
        facturaNumber = lineas2[0].split()[1]
        fecha = lineas2[1].split()[1]
        print(fecha)
        print(facturaNumber)
        
        for i in   sec[1: (len(sec) -1)]:
            partes[1] = str(partes[1])+ str(' ') + str(i)
        partes[2] = sec[len(sec)-1]
        
        partes[3] = facturaNumber
        partes[4] = fecha

        processed_data2.append(partes)



    df2 = pd.DataFrame(processed_data, columns = headers)
    df3 = pd.DataFrame(processed_data2, columns = headers)
    df4 = pd.concat([df2, df3])
    df4 = df4.reset_index(drop = True)
    print(df4)
    df5 = pd.read_excel('webPrebel/2. BASE_DATOS_FACTURAS.xlsx')
    print(df5)

    # Merge de los DataFrames para completar información faltante en df5
    df5_completado = pd.merge(df5, df4[['codigo_producto', 'fecha_compra', 'numero_factura']], 
                            on='codigo_producto', how='left', suffixes=('', '_df4'))

    # Completar las columnas faltantes en df5 con los valores de df4
    df5_completado['fecha_compra'] = df5_completado['fecha_compra'].combine_first(df5_completado['fecha_compra_df4'])
    df5_completado['numero_factura'] = df5_completado['numero_factura'].combine_first(df5_completado['numero_factura_df4'])

    # Eliminar columnas adicionales usadas para el merge
    df5_completado = df5_completado.drop(columns=['fecha_compra_df4', 'numero_factura_df4'])

    return df5_completado


def punto1(request):
    logicapunto1()
    return render(request, 'punto1.html')
    

def punto3(request):

    df = logicapunto1()
    
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
    
