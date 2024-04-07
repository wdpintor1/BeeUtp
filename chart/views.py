from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseNotFound
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.contrib.auth.decorators import login_required
from .forms import GraficaForm
from django.contrib import messages
from manage.models import TB_BEE_GRAFICA, TB_BEE_MEDIDAS, TB_BEE_CAMPOS
from django.db import transaction

def chart(request):
    chart1={'id': 1,'tituloGrafica': 'temperatura'}
    charts = {'chart1':chart1}
    return render(request, 'chart.html',{
            "tituloGrafica": "Datos a graficar",
            'charts':charts
    })
    
@csrf_exempt
def obtener_datos(request, id_canal):
    breadcrumbs = [{'url': 'lista_canales', 'label': 'Canales', 'actual':'Graficas canal'}]
    charts = []
    fechas=[]
    medidas_valores=[]
    fields = {}
    form = GraficaForm(id_canal, initial={'idCanal': id_canal})
    try:
        # Consultar TB_BEE_GRAFICOS con el id_canal y el idCampo
        graficas = TB_BEE_GRAFICA.objects.filter(idCampo__idCanal__idCanal=id_canal, idCampo__activo=True).order_by('idGrafica')         
        #Aca implementaría la logica de tiempo real
        if len(request.GET) > 0:            
            contador = 1  # Inicializa el contador
            for key, value in request.GET.items():
                if 'field' in key:
                    # Agrega el valor al diccionario fields usando el contador
                    fields[key] = float(value)
                    contador += 1  # Incrementa el contador
            contador=1          
            #Aca ingresamos los valores de los fields en la BD  
            for key, value in fields.items():
                try:
                    campo = TB_BEE_CAMPOS.objects.get(idCanal=id_canal, urlName=key)
                    # Si llegamos aquí, significa que se encontró un resultado
                    medida = TB_BEE_MEDIDAS(idCampo=campo, valor=value)
                    medida.save()
                except TB_BEE_CAMPOS.DoesNotExist:
                    # Si no se encuentra ningún resultado, puedes manejarlo aquí
                    print(f"No se encontró el campo con idCanal={id_canal} y urlName={key}")
            # Itera sobre los graficos obtenidos            
            for grafico in graficas:  
                for key, value in fields.items():
                    if grafico.idCampo.urlName == key:            
                        # Verifica si hay un valor correspondiente en fields para el gráfico actual
                        medida = fields.get(grafico.idCampo.urlName)
                        if medida is not None:
                            # Crea el objeto de datos del gráfico
                            charts.append({
                                'id': grafico.idGrafica,  
                                'tituloGrafica': grafico.titulo,
                                'medida': medida
                            })
                        contador += 1  # Incrementa el contador
        else:
                for grafico in graficas:
                        num_datos = int(grafico.Datos)
                        # Ajusta la consulta para obtener un número específico de registros
                        medidas = TB_BEE_MEDIDAS.objects.filter(idCampo=grafico.idCampo)[:num_datos]  
                        if medidas.exists():
                            fechas= [medida.fecha.strftime('%Y-%m-%dT%H:%M:%S') for medida in medidas]
                            # Deserializar las medidas a un array de Python
                            medidas_valores = [medida.valor for medida in medidas]
                        # Suponiendo que grafico.idCampo es un objeto de tipo TB_BEE_CAMPOS
                        id_campo_valor = grafico.idCampo.idCampo  # Extraer el valor de la clave primaria
                        campos = TB_BEE_CAMPOS.objects.filter(idCampo=id_campo_valor) 
                        charts.append({
                                'id': grafico.idGrafica,
                                'tituloGrafica': grafico.titulo,
                                'fechas':fechas,
                                'medidas': medidas_valores,
                                'ejeX':grafico.ejeX,
                                'ejeY':grafico.ejeY,
                                'color':grafico.color,
                                'backGround':grafico.backGround,
                                'tipo':grafico.Tipo,
                                'urlName':campos[0].urlName.capitalize(),
                        })
                        #print(charts)
        # Enviar datos al grupo WebSocket
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(f"group_{id_canal}",
        {
            "type": "chat.message",
            "message": charts,
        },
        )      
        
        return render(request, 'chart.html', {
            "tituloGrafica": "Datos a graficar",
            'charts': charts,
            'idCanal': id_canal,
            'form': form,
            'breadcrumbs':breadcrumbs
        })

    except Exception as e:
        # Manejar la excepción general
        messages.error(request, f"Error al obtener datos: {e}")

    return render(request, 'chart.html', {
            "tituloGrafica": "Datos a graficar",
            'charts': charts,
            'idCanal': id_canal,
            'form': form,
            'breadcrumbs':breadcrumbs
     })
        
@login_required       
def crear_grafica(request, id_canal):
    try:
        if request.method == 'POST':
            request.POST = request.POST.copy()
            request.POST['Tipo'] = 'line'
            form = GraficaForm(id_canal, request.POST, initial={'idCanal': id_canal}) 
            
            print(form.is_valid())
            if form.is_valid():
                grafica = form.save()
                messages.success(request, '¡Éxito al crear visualización!')
                return redirect('graficas_canal',id_canal=id_canal)           
        else:
            messages.error(request, '¡Error al enviar los datos de la gráfica!')
            return render(request, 'chart.html', {
                'claseMsj': 'alert alert-danger',
                'idCanal': id_canal
            }) 
        form = GraficaForm(id_canal, initial={'idCanal': id_canal})
        return render(request, 'chart.html', {
                'form': form,
                'idCanal': id_canal
        })
    except Exception as e:
        messages.error(request, f"Error inesperado: {e}")
        return render(request, 'chart.html', {
                'form': form,
                'idCanal': id_canal
        })

@login_required 
def editar_visualizacion(request, id_chart, id_canal): 
    try:
            # Consulta el objeto TB_BEE_GRAFICA basado en el id_chart
            grafica_instance = TB_BEE_GRAFICA.objects.get(idGrafica=id_chart)            
    except TB_BEE_GRAFICA.DoesNotExist:
            # Manejo de la excepción: por ejemplo, redireccionar a una página de error o devolver un 404
            return HttpResponseNotFound('No se encontró la gráfica') 
    if request.method == 'POST':
        request.POST = request.POST.copy()
        request.POST['Tipo'] = 'line'
        form = GraficaForm(id_chart, request.POST, instance=grafica_instance)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Éxito al editar visualización!')
            return redirect('graficas_canal',id_canal=id_canal) 
    else: 
        # Verifica si el formulario se utiliza para mostrar datos (no procesar datos del usuario)
        form = GraficaForm(id_canal, instance=grafica_instance)

    return render(request, 'editar_visualizacion.html', {
        'form': form,
        'id_canal':id_canal,
        'id_chart':id_chart
    })