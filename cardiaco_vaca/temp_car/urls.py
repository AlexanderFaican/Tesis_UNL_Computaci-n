# En temperature_app/urls.py
from django.conf import settings
from . import views
from django.contrib import messages, admin
from django.contrib.messages import success
from django.views.static import serve
from temp_car.views import *
from django.urls import include, path, re_path, reverse
#from turisticos.agenda.views import 
from django.contrib.auth.views import LoginView
from .views import LoginView
from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView


urlpatterns = [
    #path('', home, name='home'),
    path('', LoginView.as_view(),name='login'),
    #path('login/', LoginView.as_view(), name='login'),
    path('api/login/', LoginView1.as_view(), name='api-login'),
    #path('api/login/', LoginView.as_view(), name='api-login'),

    #DASBOAR DE USUARIOS
    path('frecuencia/', frecuencia, name='frecuencia'),    
    path('crear_usuario2/', crear_usuario2, name='crear_usuario2'),
    path('crear_usuario/', crear_usuario, name='crear_usuario'),
    path('temperatura/', temperatura, name='temperatura'),    
    path('monitoreo_actual/', monitoreo_actual, name='monitoreo_actual'),
    path('reportes/', reportes, name='reportes'),
    #SOLO APIS DE DATOS
    path('api/datos3/', views.obtener_datos_json3, name='obtener_datos_json3'),
    path('api/datos3/id1', views.datos3_id1, name='datos3_id1'),
    path('api/datos3/id2', views.datos3_id2, name='datos3_id2'),
    path('TemperaturaListView/', TemperaturaListView.as_view(), name='TemperaturaListView'),
    path('datos-temperatura/', TemperatureDataView.as_view(), name='temperature_data_post'),
    path('pulsaciones_list/', views.pulsaciones_list, name='pulsaciones_list'),
    path('pulsaciones_list2/', views.pulsaciones_list2, name='pulsaciones_list2'),
    path('api/', views.pulsaciones_api, name='pulsaciones_api'),  # Nueva URL para la API REST
    path('datos/', views.recibir_datos, name='recibir_datos'),
    path('mostrar_datos/', views.mostrar_datos, name='mostrar_datos'),
    path('mostrar_datos1/', views.mostrar_datos1, name='mostrar_datos1'),
    path('api/datos/', views.obtener_datos_json, name='obtener_datos_json'),
    path('api/datos2/', views.obtener_datos_json2, name='obtener_datos_json2'),
    path('recibir_datos/', views.recibir_datos2, name='recibir_datos2'),
    #Usuarios modelos User
    path('lista_usuarios/', lista_usuarios, name='lista_usuarios'),
    path('editar_usuario/<int:user_id>/', editar_usuario, name='editar_usuario'),
    path('eliminar_usuario/<int:user_id>/', eliminar_usuario, name='eliminar_usuario'),
    path('gestionar_usuarios/', gestionar_usuarios, name='gestionar_usuarios'),
    path('editar_usuario2/<int:user_id>/', editar_usuario2, name='editar_usuario2'),
    path('dashboard_redirect/', dashboard_redirect, name='dashboard_redirect'),
    #restablecer contraseña
    path('reset-password/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('reset-password/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset-password/confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset-password/complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('generar_pdf/', reporte_pdf, name='generar_pdf'),
]
