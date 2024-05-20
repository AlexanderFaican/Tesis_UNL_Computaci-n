from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.shortcuts import render
from django.views.generic import ListView
from .models import *
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib import messages
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime
from django.contrib.auth.views import LoginView
from .forms import *
from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from .models import MedicionCompleto
from io import BytesIO
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .models import CustomUser

def es_Admin(user):
    return user.groups.filter(name='Admin').exists()

def es_User(user):
    return user.groups.filter(name='User').exists()


def dashboard_redirect(request):
    # Verifica el grupo del usuario y redirige a la página correspondiente
    if request.user.groups.filter(name='Admin').exists():
        return redirect('monitoreo_actual')
    elif request.user.groups.filter(name='User').exists():
        return redirect('lista_usuarios')
    else:
        # Redirige a una página predeterminada si no pertenece a ningún grupo específico
        return redirect('login')
        
class LoginView1(APIView):
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return Response({'detail': 'Authentication successful'}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return Response({'detail': 'Authentication successful'}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
def home(request):
    return render(request, 'index.html')

@login_required
@user_passes_test(es_User)
def monitoreo_actual(request):
    return render(request, 'panel_tecnico_docente/monitoreo_reciente.html')


@login_required
@user_passes_test(es_User)
def reportes(request):
    # Obtener la página actual de la URL, por ejemplo, "/reportes/?page=2"
    page = request.GET.get('page', 1)

    # Obtener la fecha de búsqueda desde el formulario
    fecha_busqueda = request.GET.get('fecha_busqueda')

    # Obtener todos los reportes (o filtrar según tus necesidades)
    reportes_list = MedicionCompleto.objects.all().order_by('-fecha_creacion')

    # Filtrar los reportes por fecha si se proporciona una fecha de búsqueda
    if fecha_busqueda:
        try:
            fecha_busqueda = datetime.strptime(fecha_busqueda, '%Y-%m-%d')
            reportes_list = reportes_list.filter(fecha_creacion__date=fecha_busqueda)
        except ValueError:
            # Manejar el caso en que la fecha proporcionada no sea válida
            pass

    # Configurar la paginación
    paginator = Paginator(reportes_list, 10)  # Muestra 10 elementos por página
    try:
        reportes = paginator.page(page)
    except PageNotAnInteger:
        # Si la página no es un número entero, muestra la primera página
        reportes = paginator.page(1)
    except EmptyPage:
        # Si la página está fuera de rango, muestra la última página
        reportes = paginator.page(paginator.num_pages)

    context = {
        'reportes': reportes,
        'fecha_busqueda': fecha_busqueda,
    }

    return render(request, 'panel_tecnico_docente/reportes.html', context)

@login_required
@user_passes_test(es_User)
def temperatura(request):
    try:
        # Obtener la página actual desde la solicitud GET
        page = request.GET.get('page', 1)

        # Obtener todos los reportes ordenados por fecha de creación descendente
        reportes_list = MedicionCompleto.objects.all().order_by('-fecha_creacion')

        # Configurar la paginación (muestra 10 elementos por página)
        paginator = Paginator(reportes_list, 10)

        # Obtener la página solicitada
        reportes = paginator.page(page)

    except PageNotAnInteger:
        # Si la página no es un número entero, mostrar la primera página
        reportes = paginator.page(1)

    except EmptyPage:
        # Si la página está fuera de rango, mostrar la última página
        reportes = paginator.page(paginator.num_pages)

    except Exception as e:
        # Manejar cualquier otro error que pueda ocurrir durante la obtención de datos
        print(f"Error al obtener reportes: {e}")
        reportes = []

    context = {
        'reportes': reportes,
    }

    # Renderizar la plantilla y pasar el contexto
    return render(request, 'panel_tecnico_docente/temperatura.html', context)

@login_required
@user_passes_test(es_User)
def frecuencia(request):
    try:
        # Obtener la página actual desde la solicitud GET
        page = request.GET.get('page', 1)

        # Obtener todos los reportes ordenados por fecha de creación descendente
        reportes_list = MedicionCompleto.objects.all().order_by('-fecha_creacion')

        # Configurar la paginación (muestra 10 elementos por página)
        paginator = Paginator(reportes_list, 10)

        # Obtener la página solicitada
        reportes = paginator.page(page)

    except PageNotAnInteger:
        # Si la página no es un número entero, mostrar la primera página
        reportes = paginator.page(1)

    except EmptyPage:
        # Si la página está fuera de rango, mostrar la última página
        reportes = paginator.page(paginator.num_pages)

    except Exception as e:
        # Manejar cualquier otro error que pueda ocurrir durante la obtención de datos
        print(f"Error al obtener reportes: {e}")
        reportes = []

    context = {
        'reportes': reportes,
    }

    return render(request, 'panel_tecnico_docente/frecuencia.html', context)

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationFormWithExtras

def crear_usuario2(request):
    if request.method == 'POST':
        form = CustomUserCreationFormWithExtras(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('login')
    else:
        form = CustomUserCreationFormWithExtras()

    return render(request, 'admin_1/crear_usuario2.html', {'form': form})

def crear_usuario(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            # Obtén los datos del formulario
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            cedula = form.cleaned_data.get('cedula', '')  # Obtén el valor de cédula, si se proporciona
            telefono = form.cleaned_data.get('telefono', '')  # Obtén el valor de teléfono, si se proporciona

            # Crea un nuevo usuario
            user = CustomUser.objects.create_user(
                username=username,
                password=password,
                email=email,
                first_name=first_name,
                last_name=last_name,
                cedula=cedula,
                telefono=telefono
            )

            # Guarda el usuario
            user.save()

            return redirect('login')
    else:
        # Si el método no es POST, muestra el formulario en blanco
        form = UserCreationForm()

    return render(request, 'admin_1/crear_usuario.html', {'form': form})

class TemperaturaListView(ListView):
    model = TemperatureData
    template_name = 'temperatura.html'
    context_object_name = 'TemperaturaListView'
    ordering = ['-timestamp']

class TemperatureDataView(View):
    def post(self, request):
        temperatura = request.POST.get('temperature')
        if temperatura:
            TemperatureData.objects.create(temperature=temperatura)
            return render(request, 'temperature_form.html', {'message': 'Datos de temperatura guardados correctamente.'})
        else:
            return render(request, 'temperature_form.html', {'error_message': 'Datos de temperatura inválidos.'})

@login_required
def pulsaciones_list2(request):
    pulsaciones = Pulsacion.objects.all()
    pulsaciones_data = [p.pulsaciones_por_minuto for p in pulsaciones]
    return render(request, 'pulsaciones_list2.html', {'pulsaciones': pulsaciones_data})

@login_required
def pulsaciones_list(request):
     pulsaciones = Pulsacion.objects.all()
     return render(request, 'pulsaciones_list.html', {'pulsaciones': pulsaciones})

# @csrf_exempt  # Desactiva el mecanismo CSRF para recibir solicitudes POST
# def pulsaciones_list(request):
#     if request.method == 'POST':
#         data = request.POST  # Obtiene los datos enviados por el ESP32
#         pulsaciones_por_minuto = int(data.get('pulsaciones', 0))  # Suponemos que el valor de pulsaciones se envía en el campo 'pulsaciones'

#         # Guarda los datos en la base de datos
#         if pulsaciones_por_minuto > 0:
#             pulsacion = Pulsacion(pulsaciones_por_minuto=pulsaciones_por_minuto)
#             pulsacion.save()

#             return JsonResponse({'message': 'Datos guardados correctamente.'})
#         else:
#             return JsonResponse({'message': 'Datos inválidos.'}, status=400)

#     else:
#         pulsaciones = Pulsacion.objects.all()
#         return render(request, 'pulsacicones_list.html', {'pulsaciones': pulsaciones})
@csrf_exempt
def pulsaciones_api(request):
    if request.method == 'POST':
        data = request.POST
        pulsaciones_por_minuto = int(data.get('pulsaciones', 0))

        if pulsaciones_por_minuto > 0:
            pulsacion = Pulsacion(pulsaciones_por_minuto=pulsaciones_por_minuto)
            pulsacion.save()

            return JsonResponse({'message': 'Datos guardados correctamente.'})
        else:
            return JsonResponse({'message': 'Datos inválidos.'}, status=400)

    else:
        return JsonResponse({'message': 'Método no permitido.'}, status=405)
    
@csrf_exempt
def recibir_datos(request):
    if request.method == 'POST':
        humedad = request.POST.get('humedad')
        temperatura = request.POST.get('temperatura')

        if humedad is not None and temperatura is not None:
            Medicion.objects.create(humedad=humedad, temperatura=temperatura)
            return JsonResponse({'mensaje': 'Datos guardados exitosamente.'})
        else:
            return JsonResponse({'error': 'Datos incompletos.'})

    return JsonResponse({'error': 'Solicitud no permitida.'}, status=405)

@csrf_exempt  # Esto es para deshabilitar la protección CSRF en esta vista (deberías tomar medidas de seguridad apropiadas en un entorno de producción)
def recibir_datos2(request):
    if request.method == 'POST':
        collar_id = request.POST.get('collar_id')
        nombre_vaca = request.POST.get('nombre_vaca')
        temperatura = request.POST.get('temperatura')
        pulsaciones = request.POST.get('pulsaciones')

        if temperatura is not None and pulsaciones is not None and collar_id is not None:
            MedicionCompleto.objects.create(
                collar_id=collar_id,
                nombre_vaca=nombre_vaca,
                temperatura=temperatura,
                pulsaciones=pulsaciones
            )
            return JsonResponse({'mensaje': 'Datos guardados exitosamente.'})
        else:
            return JsonResponse({'error': 'Datos incompletos.'})
    return JsonResponse({'error': 'Solicitud no permitida.'}, status=405)

@login_required
def mostrar_datos(request):
    datos = Medicion.objects.all()
    return render(request, 'mostrar_datos.html', {'datos': datos})

@login_required
def mostrar_datos1(request):
    datos = Medicion.objects.all()
    return render(request, 'mostrar_datos_completos.html', {'datos': datos})

@login_required
def obtener_datos_json(request):
    datos = Medicion.objects.all()
    datos_json = [{'id': dato.id, 'temperatura': dato.temperatura, 'humedad': dato.humedad} for dato in datos]
    return JsonResponse(datos_json, safe=False)

@login_required
def obtener_datos_json2(request):
    datos = MedicionCompleto.objects.all().order_by('-fecha_creacion')[:1]  # Obtener solo el último dato
    if datos:
        ultimo_dato = datos[0]
        data = {
            'temperatura': ultimo_dato.temperatura,
            'pulsaciones': ultimo_dato.pulsaciones,
        }
        return JsonResponse(data)
    else:
        return JsonResponse({'error': 'No hay datos disponibles'})

def obtener_datos_json3(request):
    fecha_busqueda = request.GET.get('fecha', None)

    if fecha_busqueda:
        # Filtrar por fecha si se proporciona
        datos = MedicionCompleto.objects.filter(fecha_creacion__date=fecha_busqueda).order_by('-fecha_creacion')
    else:
        # Obtener todos los datos si no se proporciona fecha
        datos = MedicionCompleto.objects.all().order_by('-fecha_creacion')

    if datos:
        reportes = []
        for dato in datos:
            reporte = {
                'fecha_creacion': dato.fecha_creacion.strftime('%Y-%m-%d %H:%M:%S'),
                'temperatura': dato.temperatura,
                'nombre_vaca': dato.nombre_vaca,
                'pulsaciones': dato.pulsaciones,
                'collar_id': dato.collar_id,
            }
            reportes.append(reporte)
        return JsonResponse({'reportes': reportes})
    else:
        return JsonResponse({'error': 'No hay datos disponibles'})


def datos3_id1(request):
    fecha_busqueda = request.GET.get('fecha', None)

    if fecha_busqueda:
        # Filtrar por fecha si se proporciona
        datos = MedicionCompleto.objects.filter(fecha_creacion__date=fecha_busqueda, collar_id=1).order_by('-fecha_creacion')
    else:
        # Obtener todos los datos si no se proporciona fecha
        datos = MedicionCompleto.objects.filter(collar_id=1).order_by('-fecha_creacion')

    if datos:
        reportes = []
        for dato in datos:
            reporte = {
                'fecha_creacion': dato.fecha_creacion.strftime('%Y-%m-%d %H:%M:%S'),
                'temperatura': dato.temperatura,
                'nombre_vaca': dato.nombre_vaca,
                'pulsaciones': dato.pulsaciones,
                'collar_id': dato.collar_id,
            }
            reportes.append(reporte)
        return JsonResponse({'reportes': reportes})
    else:
        return JsonResponse({'error': 'No hay datos disponibles'})


def datos3_id2(request):
    fecha_busqueda = request.GET.get('fecha', None)

    if fecha_busqueda:
        # Filtrar por fecha si se proporciona
        datos = MedicionCompleto.objects.filter(fecha_creacion__date=fecha_busqueda, collar_id=2).order_by('-fecha_creacion')
    else:
        # Obtener todos los datos si no se proporciona fecha
        datos = MedicionCompleto.objects.filter(collar_id=2).order_by('-fecha_creacion')

    if datos:
        reportes = []
        for dato in datos:
            reporte = {
                'fecha_creacion': dato.fecha_creacion.strftime('%Y-%m-%d %H:%M:%S'),
                'temperatura': dato.temperatura,
                'nombre_vaca': dato.nombre_vaca,
                'pulsaciones': dato.pulsaciones,
                'collar_id': dato.collar_id,
            }
            reportes.append(reporte)
        return JsonResponse({'reportes': reportes})
    else:
        return JsonResponse({'error': 'No hay datos disponibles'})


#usuarios

@login_required
@user_passes_test(es_Admin)
def gestionar_usuarios(request):
    usuarios = User.objects.all()
    return render(request, 'usuarios/listar_usuarios_2.html', {'usuarios': usuarios})

@login_required
@user_passes_test(es_Admin)
def lista_usuarios(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        user = User.objects.get(id=user_id)

        # Cambiar el estado activo/inactivo del usuario
        user.is_active = not user.is_active
        user.save()

        messages.success(request, f'Estado de {user.username} actualizado correctamente.')

        return redirect('lista_usuarios')

    usuarios = User.objects.all()
    return render(request, 'usuarios/lista_usuarios.html', {'usuarios': usuarios})

@login_required
@user_passes_test(es_Admin)
def editar_usuario(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario actualizado correctamente.')
            return redirect('gestionar_usuarios')
    else:
        form = UserChangeForm(instance=user)

    return render(request, 'usuarios/editar_usuario.html', {'form': form, 'user': user})

@login_required
@user_passes_test(es_Admin)
def editar_usuario2(request,user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save()
            # Loguear al usuario automáticamente después de registrarse (opcional)
            username = form.cleaned_data.get('username')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            email = form.cleaned_data.get('email')         
            password = form.cleaned_data.get('password1')

            user = authenticate(request, username=username,first_name=first_name,last_name=last_name, email=email, password=password)
            login(request, user)
            return redirect('gestionar_usuarios')  # Redirige a donde desees después de registrarse
    else:
        form = CustomUserCreationForm(instance=user)

    return render(request, 'usuarios/editar_usuario2.html', {'form': form, 'user': user})

@login_required
@user_passes_test(es_Admin)
def eliminar_usuario(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        user.delete()
        messages.success(request, 'Usuario eliminado correctamente.')
        return redirect('gestionar_usuarios')

    return render(request, 'usuarios/eliminar_usuario.html', {'user': user})
# IMPRIMIR LOS DATOS 
def render_to_pdf(html_content, context_dict={}):
    header_html = """
<table style="width: 100%; border-collapse: collapse;">
    <tr>
        <td style="padding: 10px;">
            <img src="./temp_car/static/assets/img/logounl.png" alt="Left Logo" style="width: 195px; height: auto; margin-right: 10px;">
        </td>
        <td style="padding: 10px; vertical-align: top; text-align: right;">
            <img src="./temp_car/static/assets/img/logoComputacion.png" alt="Right Logo" style="width: 100px; height: auto; margin-left: 10px;">
        </td>
    </tr>
</table>
<div style="text-align: center; margin: 20px 0;">
    <h1 style="font-size: 24px; color: #333; margin: 0;">Reporte de Monitoreos al Ganado Bovino Lechero</h1>
</div>

"""

    full_html = header_html + html_content

    footer_html = """
        <footer style="text-align: center; margin-top: 20px; background-color: #f8f8f8; padding: 10px;">
            <p style="font-size: 12px; color: #white; margin: 0;">© All rights reserved | Carrera de Ingeniería en Computación</p>
        </footer>
    """

    full_html += footer_html

    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(full_html.encode("ISO-8859-1")), result)

    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

def reporte_pdf(request):
    fecha_busqueda = request.GET.get('fecha_busqueda')
    reportes = MedicionCompleto.objects.all()

    if fecha_busqueda:
        reportes = reportes.filter(fecha_creacion__date=fecha_busqueda)

    context = {
        'reportes': reportes,
        'fecha_busqueda': fecha_busqueda,
    }

    table_content = get_template('panel_tecnico_docente/reportes.html').render(context).split('<table id="tablaReportes">')[1].split('</table>')[0]
    table_content = table_content.replace('<th>', '<th style="padding: 8px; text-align: center; background-color: #72b4fc;">')
    table_content = table_content.replace('<td>', '<td style="padding: 8px; text-align: center; border: 1px solid #ddd;">')
    table_html = f'<table id="tablaReportes" style="width: 80%; margin: 20px auto; border-collapse: collapse;">{table_content}</table>'

    pdf = render_to_pdf(table_html, context)

    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = f"reporte_monitoreos_{fecha_busqueda or datetime.now().strftime('%Y-%m-%d')}.pdf"
        content = f'attachment; filename="{filename}"'
        response['Content-Disposition'] = content
        return response

    return HttpResponse("Error al generar el PDF.", status=500)