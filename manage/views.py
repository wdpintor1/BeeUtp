from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login as login_django
from django.contrib.auth import logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import CustomAuthenticationForm
from django.contrib import messages
from .models import TB_BEE_CANALES,TB_BEE_CAMPOS
from .models import TB_BEE_GRAFICA

from .forms import CanalForm, CanalEditForm, CampoForm, CustomUserCreationForm
from django.core.paginator import Paginator, EmptyPage
from django import forms
from django.db import transaction
from django.forms import modelformset_factory,modelform_factory
import logging
from redis.exceptions import ConnectionError

logger = logging.getLogger(__name__)


# Create your views here.
def login(request):
     return render(request, 'login.html',{
            'form': CustomAuthenticationForm 
        })
@login_required
def home(request):
    return render(request,'home.html')

def registro(request):
    if request.method == 'GET':
        return render(request, 'registro.html',{
            'form': CustomUserCreationForm 
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user= User.objects.create_user(username=request.POST['username'],password=request.POST['password1'])
                user.save()
                login_django(request, user)                
                return redirect('home')
            except:
                return render(request, 'registro.html',{
                    'form': CustomUserCreationForm,
                    'mensaje': 'El usuario que intenta crear ya existe!' 
                })
                messages.info(request, "El usuario que intenta crear ya existe!")
        else:
            return render(request, 'registro.html',{
                    'form': CustomUserCreationForm,
                    'mensaje': 'Las contraseñas no coinciden' 
            })
            messages.info(request, "Las contraseñas no coinciden")
            
def signin(request):
    if request.method == 'GET':
        return render(request, 'login.html',{
            'form': CustomAuthenticationForm 
        })
    else:       
        user= authenticate(request, username=request.POST['username'], password=request.POST['password'])  
        try:            
            if user is None:
                messages.error(request, '¡El usuario o la contraseña son inválidos!')
                return render(request, 'login.html',{
                'form': CustomAuthenticationForm,
                'claseMsj': 'alert alert-danger' 
                }) 
            else:
                login_django(request, user)
                return lista_canales(request)
        except ConnectionError as e:
            # Aquí manejas la excepción ConnectionError
            # Por ejemplo, puedes agregar un mensaje de error para el usuario
            if user is None:
                messages.error(request, 'Error de conexión al servidor de redis.')
                return render(request, 'login.html', {'form': CustomAuthenticationForm, 'claseMsj': 'alert alert-danger'})
            else:    
                login_django(request, user)            
                return render(request, 'home.html')
            
            
@login_required(login_url= 'login')
def signout(request):
	logout(request)
	return redirect('signin')

@login_required
def lista_canales(request):
    # Filtra los canales por el usuario que ha iniciado sesión y los ordena por fecha de actualización descendente
    canales = TB_BEE_CANALES.objects.filter(idUsuario=request.user).order_by('-fecha_actualizacion')    
    # Configura la paginación
    page = request.GET.get('page', 1)
    paginator = Paginator(canales, 5)  # Muestra 5 canales por página   
    try:
        canales = paginator.page(page)
    except EmptyPage:
        canales = paginator.page(paginator.num_pages)
    
    return render(request, 'home.html', {'canales': canales})

@login_required
def crear_canal(request):
    if request.method == 'POST':
        form = CanalForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    # Guardar el canal en TB_BEE_CANALES
                    canal = TB_BEE_CANALES(nombre=request.POST['nombre'], descripcion=request.POST['descripcion'], idUsuario=request.user)
                    canal.save()

                    # Crear campos dinámicos asociados al canal en TB_BEE_CAMPOS
                    for i in range(1, CanalForm.num_campos_adicionales + 1):
                        campo_name = f'campo_adicional_{i}'
                        activo_name = f'activo_campo_adicional_{i}'

                        nombre_campo = form.cleaned_data[campo_name]
                        activo_campo = form.cleaned_data[activo_name]
                        urlName= f'field{i}'
                        # Crear el campo en TB_BEE_CAMPOS asociado al canal
                        campo_creado=TB_BEE_CAMPOS.objects.create(
                            nombre=nombre_campo,
                            idCanal=canal,
                            activo=activo_campo,
                            urlName=urlName
                            # Puedes establecer otros campos según tu modelo
                        )
                        #Aca vamos a crear una gráfica por cada campo
                        TB_BEE_GRAFICA.objects.create(
                            titulo=nombre_campo,
                            ejeX= 'Tiempo',
                            ejeY=nombre_campo,
                            color='#000000',
                            backGround='#FFFFFF',
                            Tipo='line',
                            Datos=20,
                            idCampo=campo_creado
                        )

                messages.success(request, '¡Canal creado con éxito!', extra_tags='claseMsj')
                return redirect('lista_canales')
            except Exception as e:
                messages.error(request, f'Error al crear el canal: {str(e)}', extra_tags='claseMsj')
    else:
        form = CanalForm()

    breadcrumbs = [{'url': 'lista_canales', 'label': 'Canales', 'actual':'Crear canal'}]
    return render(request, 'crear_canal.html', {
        'form': form,
        'breadcrumbs': breadcrumbs
    })
    
@login_required
def editar_canal(request, id_canal):
    breadcrumbs = [{'url': 'lista_canales', 'label': 'Canales', 'actual': 'Configurar canal'}]
    try:
        canal = get_object_or_404(TB_BEE_CANALES, idCanal=id_canal)
        if request.method == 'POST':
            form = CanalEditForm(request.POST, instance=canal) 
            # Obtén los datos del request.POST
            formset_data = request.POST.copy()           
            # Elimina los campos "nombre" y "descripcion"
            del formset_data['nombre']
            del formset_data['descripcion']  
            CampoFormSet = modelformset_factory(TB_BEE_CAMPOS, form=CampoForm, extra=0)            
            formset = CampoFormSet(formset_data, prefix='campo_formset')                    
            if form.is_valid() and formset.is_valid():
                #print("re valido")
                # Guardar los campos adicionales
                for form_campo in formset:
                    #print("no entra")
                    #print(form_campo.errors)
                    campo = form_campo.save(commit=False)
                    campo.idCanal = canal
                    campo.save()  
                    # Aquí actualizas TB_BEE_GRAFICA con el valor de campo.nombre
                    TB_BEE_GRAFICA.objects.filter(idCampo=campo.idCampo).update(ejeY=campo.nombre, titulo=campo.nombre)                 
                    
                form.save()
                messages.success(request, '¡El canal y los campos fueron modificados con éxito!', extra_tags='claseMsj')
                return redirect('editar_canal', id_canal=canal.idCanal)
        else:
            form = CanalEditForm(instance=canal)
            CampoFormSet = modelformset_factory(TB_BEE_CAMPOS, form=CampoForm, extra=0)             
            formset = CampoFormSet(queryset=TB_BEE_CAMPOS.objects.filter(idCanal=canal), prefix='campo_formset')           
        return render(request, 'editar_canal.html', {
            'form': form,
            'formset': formset,
            'breadcrumbs': breadcrumbs
        })
    except Exception as e:
        # O registrar la excepción en un archivo de registro
        logger.exception(f'Error en la vista: {str(e)}')
        messages.error(request, f'Error en la vista: {str(e)}', extra_tags='claseMsj')
        return redirect('home')
    
@login_required
def eliminar_canal(request, id_canal):
    try:
        canal = get_object_or_404(TB_BEE_CANALES, idCanal=id_canal)
        # Eliminar canal y manejar otras operaciones relacionadas si es necesario
        canal.delete()
        messages.success(request, '¡El canal fue eliminado con éxito!', extra_tags='claseMsj')
        return redirect('home')
    except Exception as e:
        # Manejar la excepción y mostrar un mensaje de error adecuado
        messages.error(request, f'Error al eliminar el canal: {str(e)}', extra_tags='claseMsj')
        # Puedes redirigir a una página de error o mostrar un mensaje en la misma página
        return redirect('home')