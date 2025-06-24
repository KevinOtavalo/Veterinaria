from django.urls import path
from . import views

urlpatterns = [
    path('', views.vista_publica, name='vista_publica'),
    path('mis-mascotas/', views.vista_mascotas, name='vista_mascotas'),
    path('mascota/registrar/', views.registrar_mascota, name='registrar_mascota'),
    path('mascota/<int:mascota_id>/',
         views.detalle_mascota, name='detalle_mascota'),
    path('mascota/editar/<int:mascota_id>/',
         views.editar_mascota, name='editar_mascota'),
    path('mascota/eliminar/<int:mascota_id>/',
         views.eliminar_mascota, name='eliminar_mascota'),
    path('mascota/<int:mascota_id>/vacuna/',
         views.registrar_vacuna, name='registrar_vacuna'),
    path('mascota/<int:mascota_id>/consulta/',
         views.registrar_consulta, name='registrar_consulta'),
    path('consulta/<int:consulta_id>/editar/',
         views.editar_consulta, name='editar_consulta'),
    path('consulta/<int:consulta_id>/eliminar/',
         views.eliminar_consulta, name='eliminar_consulta'),
    path('vacuna/<int:vacuna_id>/editar/',
         views.editar_vacuna, name='editar_vacuna'),
    path('vacuna/<int:vacuna_id>/eliminar/',
         views.eliminar_vacuna, name='eliminar_vacuna'),
    path('todas-mascotas/', views.vista_mascotas_todas,
         name='vista_mascotas_todas'),
    path('mascota/<int:mascota_id>/vacunas/',
         views.detalle_vacunas, name='detalle_vacunas'),
    path('mascota/<int:mascota_id>/consultas/',
         views.detalle_consultas, name='detalle_consultas'),

    # Puedes usar la vista pública con otro nombre si quieres que quede más claro
    path('publico/', views.vista_publica, name='publico_mascotas'),
]
