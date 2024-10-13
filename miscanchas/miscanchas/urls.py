from django.urls import include, path, re_path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from canchas.views import *
from django.contrib.auth.decorators import login_required
from allauth.account import views as allauth_views

urlpatterns = [
    path('', HomePageView.as_view(), name="home"),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('login/', allauth_views.LoginView.as_view(), name='login'),
    path('login_success/', login_success, name='login_success'),
    path('register/', new_account, name='new_account'),
    # path('new_profile/', UserProfileCreate.as_view(template_name="registration/profile_new.html"), name='create_profile'),
    path('new_profile/', create_user_profile, name='create_profile'),
    path('edit_profile/', edit_profile, name='edit_profile'),
    path('logout/', logout_and_login, name='logout_then_login'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change_form.html'), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'), name='password_change_done'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    re_path(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('owner/new/', new_owner, name='new_owner'),
    path('owner/new_profile/', OwnerProfileCreate.as_view(template_name="owner/owner_new_profile.html"), name='create_profile_owner'),

    path('owner/new_employee/', new_employee, name='new_employee'),
    path('owner/new_employee/new_profile/', EmpleadoEstablecimientoCreate.as_view(), name='new_employee_profile'),
    path('owner/employee/list/', EmpleadoEstablecimientoList.as_view(), name='employee_list'),
    path('owner/employee/<int:pk>/update/', EmpleadoEstablecimientoUpdate.as_view(), name='employee_update'),

    path('buscar/', busqueda_cancha, name='buscar_canchas'),

    path('establecimiento/<int:pk>/detail/', EstablecimientoDetailFront.as_view(), name='establecimiento_detail_fe'),
    path('establecimiento/<int:establecimiento_id>/cancha/<int:pk>/detail/', CanchaDetailFront.as_view(), name='cancha_detail_fe'),
    path('establecimiento/<int:establecimiento_id>/cancha/<int:pk>/reservar/', ReservaCreate.as_view(), name='reserva_create'),

    path('redirector/<int:pk>/', redirector, name="redirector"),
    re_path(r'^establecimiento/(?P<establecimiento_id>[0-9]+)/cancha/(?P<cancha_id>[0-9]+)/reservar/(?P<day>[0-9]{2})/(?P<month>[0-9]{2})/(?P<year>[0-9]{4})/$', disponibilidad_cancha, name='disponibilidad_cancha'),
    path('mis_reservas/', ReservaListFront.as_view(), name='reservas_list_fe'),
    path('cancelar_reserva/<int:pk>/', cancelar_reserva_fe, name="reservas_cancel_fe"),

    # MP ENDPOINTS
    path('gracias/success', gracias_mp, name='gracias_mp'),
    path('ipn', mp_notification, name='ipn'),

    # PayPal Endpoints
    path('ipn-paypal/<str:codigo_operacion>/<str:con_luz>/<str:fecha>/<int:periodo_index>/<int:cancha_id>', ipn_paypal, name='ipn_paypal'),
    path('compra-finalizada', compra_finalizada, name='compra-finalizada'),

    # Favoritos
    path('favoritos/list/', FavoritoList.as_view(), name='favorito_list'),
    path('establecimiento/<int:establecimiento_id>/cancha/<int:pk>/add_favorite/', login_required(add_fav), name='favorito_create'),
    path('favoritos/<int:pk>/delete/', FavoritoDelete.as_view(), name='favorito_delete'),

    # Backoffice
    path('backoffice/home/', HomePageBackofficeView.as_view(), name="home_backoffice"),
    path('backoffice/canchas/list/', CanchaListFull.as_view(), name="cancha_list_full_backoffice"),
    path('backoffice/canchas/new/', create_cancha_backoffice, name="cancha_create_backoffice"),

    path('backoffice/cancelaciones/', ReservasCanceladasList.as_view(), name="reservas_canceladas"),
    path('backoffice/cancelaciones/<int:pk>/update/', CancelacionesUpdate.as_view(), name="cancelaciones_update"),

    path('backoffice/facturacion_list/', FacturacionList.as_view(), name="facturacion_list"),
    path('backoffice/admin/cancelaciones/', ReservasCanceladasListFull.as_view(), name="reservas_canceladas_admin"),
    path('backoffice/admin/cancelaciones/<int:pk>/update/', CancelacionesUpdateAdmin.as_view(), name="cancelaciones_update_admin"),

    path('backoffice/reservas/json/', reservas_serialized, name='reservas_backoffice_json'),
    path('backoffice/reservas/list/', ReservaList.as_view(), name="reservas_backoffice"),
    path('backoffice/reservas/calendar/', CalendarView.as_view(), name="calendar_backoffice"),
    path('backoffice/reservas/<int:pk>/detail/', ReservaDetail.as_view(), name="reserva_detail"),
    path('backoffice/reservas/<int:pk>/update/', ReservaUpdate.as_view(), name="reserva_update"),
    path('backoffice/reservas/<int:pk>/aceptar/', aceptar_reserva, name="reserva_accept"),
    path('backoffice/reservas/<int:pk>/cancelar/', cancelar_reserva, name="reserva_cancel"),

    path('backoffice/establecimiento/new/', login_required(create_establecimiento), name='establecimiento_create'),
    path('backoffice/establecimiento/<int:pk>/full/', login_required(EstablecimientoDetail.as_view()), name='establecimiento_full'),
    path('backoffice/establecimiento/<int:pk>/detail/', login_required(EstablecimientoDetail.as_view()), name='establecimiento_detail'),
    path('backoffice/establecimiento/<int:pk>/update/', login_required(update_establecimiento), name='establecimiento_update'),
    path('backoffice/establecimiento/<int:pk>/delete/', login_required(EstablecimientoDelete.as_view()), name='establecimiento_delete'),
    path('backoffice/establecimiento/list/', login_required(EstablecimientoList.as_view()), name='establecimiento_list'),
    path('backoffice/establecimiento/<int:pk>/facturacion/', login_required(FacturacionCreate.as_view()), name='facturacion_create'),
    path('backoffice/establecimiento/<int:establecimiento_id>/facturacion/<int:pk>/update/', login_required(FacturacionUpdate.as_view()), name='facturacion_update'),

    path('backoffice/establecimiento/<int:establecimiento_id>/cancha/new/', login_required(create_cancha), name='cancha_create'),
    path('backoffice/establecimiento/<int:establecimiento_id>/cancha/<int:pk>/detail/', login_required(CanchaDetail.as_view()), name='cancha_detail'),
    path('backoffice/establecimiento/<int:establecimiento_id>/cancha/<int:pk>/update/', login_required(update_cancha), name='cancha_update'),
    path('backoffice/establecimiento/<int:establecimiento_id>/cancha/<int:pk>/delete/', login_required(CanchaDelete.as_view()), name='cancha_delete'),
    path('backoffice/establecimiento/<int:establecimiento_id>/cancha/list/', login_required(CanchaList.as_view()), name='cancha_list'),

    # Other views
    path('backoffice/soporte/', TemplateView.as_view(template_name='info/soporte.html'), name='soporte'),
    path('ayuda/', TemplateView.as_view(template_name='info/ayuda.html'), name='ayuda'),
    path('contacto/', ContactFormView.as_view(), name='contacto'),
    path('contacto/confirmacion', TemplateView.as_view(template_name='info/email_sent.html'), name='email-sent'),
    path('faq/', TemplateView.as_view(template_name='info/faq.html'), name='faq'),
    path('quienes_somos/', TemplateView.as_view(template_name='info/quienes_somos.html'), name='quienes_somos'),
    path('como_funciona/', TemplateView.as_view(template_name='info/como_funciona.html'), name='como_funciona'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
