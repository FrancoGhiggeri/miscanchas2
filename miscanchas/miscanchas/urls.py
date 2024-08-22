"""miscanchas URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views

from django.conf import settings
from canchas.views import *

from django.contrib.auth.decorators import login_required
from django.conf.urls.static import static

from django.contrib.auth.views import (login, logout_then_login, 
    password_change, password_change_done, password_reset,
    password_reset_done, password_reset_confirm, password_reset_complete)

from allauth.account import views as allauth_views


urlpatterns = [
    url(r'^$', HomePageView.as_view(), name="home"),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^login/$', allauth_views.login, name='login'),
    url(r'login_success/$', login_success, name='login_success'),
    url(r'^register/', new_account, name='new_account'),
    url(r'^new_profile/', UserProfileCreate.as_view(template_name="registration/profile_new.html"), name='create_profile'),
    url(r'^edit_profile/', edit_profile, name='edit_profile'),

    url(r'^logout/$', logout_and_login, name='logount_then_login'),
    url(r'^password_change/$', password_change,
        {'template_name': 'registration/password_change_form.html'},
        name='password_change'),
    url(r'^password_change/done/$', password_change_done,
        {'template_name': 'registration/password_change_done.html'},
        name='password_change_done'),
    url(r'^password_reset/$', password_reset),
    url(r'^password_reset/done/$', password_reset_done, 
        {'template_name': 'registration/password_reset_done.html'},
        name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', 
        password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', password_reset_complete, name='password_reset_complete'),

    url(r'^owner/new/$', new_owner, name='new_owner'),
    url(r'^owner/new_profile/', OwnerProfileCreate.as_view(template_name="owner/owner_new_profile.html"), name='create_profile_owner'),

    url(r'^owner/new_employee/$', new_employee, name='new_employee'),
    url(r'^owner/new_employee/new_profile/$', EmpleadoEstablecimientoCreate.as_view(), name='new_employee_profile'),
    url(r'^owner/employee/list/$', EmpleadoEstablecimientoList.as_view(), name='employee_list'),
    url(r'^owner/employee/(?P<pk>[0-9]+)/update/$', EmpleadoEstablecimientoUpdate.as_view(), name='employee_update'),

    url(r'^buscar/$', busqueda_cancha, name='buscar_canchas'),

    url(r'^establecimiento/(?P<pk>[0-9]+)/detail/$',
        EstablecimientoDetailFront.as_view(), name='establecimiento_detail_fe'),

    url(r'^establecimiento/(?P<establecimiento_id>[0-9]+)/cancha/(?P<pk>[0-9]+)/detail/$',
        CanchaDetailFront.as_view(), name='cancha_detail_fe'),
    #Aca es donde completaria el horario de la reserva y esas cosas
    url(r'^establecimiento/(?P<establecimiento_id>[0-9]+)/cancha/(?P<pk>[0-9]+)/reservar/$',
        login_required(ReservaCreate.as_view()), name='reserva_create'),

    url(r'^redirector/(?P<pk>[0-9]+)/$', redirector, name="redirector"),

    url(r'^establecimiento/(?P<establecimiento_id>[0-9]+)/cancha/(?P<cancha_id>[0-9]+)/reservar/(?P<day>[0-9]{2})/(?P<month>[0-9]{2})/(?P<year>[0-9]{4})/$', disponibilidad_cancha, name='disponibilidad_cancha'),
    # Esto es para mostrar una lista de las reservas que tiene el usuario
    url(r'^mis_reservas/', ReservaListFront.as_view(), name='reservas_list_fe'),
    url(r'^cancelar_reserva/(?P<pk>[0-9]+)/$', cancelar_reserva_fe, name="reservas_cancel_fe"),

    #MP ENDPOINTS
    url(r'^gracias/success$', gracias_mp, name='gracias_mp'),
    url(r'^ipn$', mp_notification, name='ipn'),

    # lista de favoritos
    url(r'^favoritos/list/', FavoritoList.as_view(), name='favorito_list'),
    # a la altura de la cancha podrias hacer click en un boton para agregarlo a favoritos
    url(r'^establecimiento/(?P<establecimiento_id>[0-9]+)/cancha/(?P<pk>[0-9]+)/add_favorite/', login_required(add_fav), name='favorito_create'),
    # desde la vista de favoritos list, podrias hacer 
    url(r'^favoritos/(?P<pk>[0-9]+)/delete/', FavoritoDelete.as_view(), name='favorito_delete'),

    url(r'^backoffice/home/$', HomePageBackofficeView.as_view(), name="home_backoffice"),
    url(r'^backoffice/canchas/list/$', CanchaListFull.as_view(), name="cancha_list_full_backoffice"),
    url(r'^backoffice/canchas/new/$', create_cancha_backoffice, name="cancha_create_backoffice"),

    url(r'^backoffice/cancelaciones/$', ReservasCanceladasList.as_view(), name="reservas_canceladas"),
    url(r'^backoffice/cancelaciones/(?P<pk>[0-9]+)/update/$', CancelacionesUpdate.as_view(), name="cancelaciones_update"),

    url(r'^backoffice/facturacion_list/$', FacturacionList.as_view(), name="facturacion_list"),
    url(r'^backoffice/admin/cancelaciones/$', ReservasCanceladasListFull.as_view(), name="reservas_canceladas_admin"),
    url(r'^backoffice/admin/cancelaciones/(?P<pk>[0-9]+)/update/$', CancelacionesUpdateAdmin.as_view(), name="cancelaciones_update_admin"),

    url(r'^backoffice/reservas/json/', reservas_serialized, name='reservas_backoffice_json'),
    # la idea es mostrar todas las reservas que tiene para todas las canchas de ese duenho
    url(r'^backoffice/reservas/list/$', ReservaList.as_view(), name="reservas_backoffice"),
    url(r'^backoffice/reservas/calendar/$', CalendarView.as_view(), name="calendar_backoffice"),
    # Detalle de una reserva desde el BE para que pueda chequear el estado
    url(r'^backoffice/reservas/(?P<pk>[0-9]+)/detail/$', ReservaDetail.as_view(), name="reserva_detail"),
    # Desde aca la puede aceptar y luego poner si asistio o no a la reserva.
    url(r'^backoffice/reservas/(?P<pk>[0-9]+)/update/$', ReservaUpdate.as_view(), name="reserva_update"),

    url(r'^backoffice/reservas/(?P<pk>[0-9]+)/aceptar/$', aceptar_reserva, name="reserva_accept"),
    url(r'^backoffice/reservas/(?P<pk>[0-9]+)/cancelar/$', cancelar_reserva, name="reserva_cancel"),

    url(r'^backoffice/establecimiento/new/$',
        login_required(create_establecimiento), name='establecimiento_create'),
    url(r'^backoffice/establecimiento/(?P<pk>[0-9]+)/full/$',
        login_required(EstablecimientoDetail.as_view()), name='establecimiento_full'),
    url(r'^backoffice/establecimiento/(?P<pk>[0-9]+)/detail/$',
        login_required(EstablecimientoDetail.as_view()), name='establecimiento_detail'),
    url(r'^backoffice/establecimiento/(?P<pk>[0-9]+)/update/$',
        login_required(update_establecimiento), name='establecimiento_update'),
    url(r'^backoffice/establecimiento/(?P<pk>[0-9]+)/delete/$',
        login_required(EstablecimientoDelete.as_view()), name='establecimiento_delete'),
    url(r'^backoffice/establecimiento/list/$',
        login_required(EstablecimientoList.as_view()), name='establecimiento_list'),
    url(r'^backoffice/establecimiento/(?P<pk>[0-9]+)/facturacion/$',
        login_required(FacturacionCreate.as_view()), name='facturacion_create'),
    url(r'^backoffice/establecimiento/(?P<establecimiento_id>[0-9]+)/facturacion/(?P<pk>[0-9]+)/update/$',
        login_required(FacturacionUpdate.as_view()), name='facturacion_update'),

    url(r'^backoffice/establecimiento/(?P<establecimiento_id>[0-9]+)/cancha/new/$', 
        login_required(create_cancha), name='cancha_create'),
    url(r'^backoffice/establecimiento/(?P<establecimiento_id>[0-9]+)/cancha/(?P<pk>[0-9]+)/detail/$', 
        login_required(CanchaDetail.as_view()), name='cancha_detail'),
    url(r'^backoffice/establecimiento/(?P<establecimiento_id>[0-9]+)/cancha/(?P<pk>[0-9]+)/update/$', 
        login_required(update_cancha), name='cancha_update'),
    url(r'^backoffice/establecimiento/(?P<establecimiento_id>[0-9]+)/cancha/(?P<pk>[0-9]+)/delete/$', 
        login_required(CanchaDelete.as_view()), name='cancha_delete'),
    url(r'^backoffice/establecimiento/(?P<establecimiento_id>[0-9]+)/cancha/list/$', 
        login_required(CanchaList.as_view()), name='cancha_list'),

    url(r'^backoffice/soporte/', TemplateView.as_view(template_name='info/soporte.html'),name='soporte'),

    url(r'^ayuda/', TemplateView.as_view(template_name='info/ayuda.html'),name='ayuda'),
    url(r'^contacto/$', ContactFormView.as_view(), name='contacto'),
    url(r'^contacto/confirmacion$', TemplateView.as_view(template_name='info/email_sent.html'), 
        name='email-sent'),


    url(r'^faq/$', TemplateView.as_view(template_name='info/faq.html'), name='faq'),
    url(r'^quienes_somos/$', TemplateView.as_view(template_name='info/quienes_somos.html'), name='quienes_somos'),
    url(r'^como_funciona/$', TemplateView.as_view(template_name='info/como_funciona.html'), name='como_funciona'),



]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
