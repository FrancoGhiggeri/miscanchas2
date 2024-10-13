# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from allauth.socialaccount.models import SocialAccount
from django.contrib.sites.models import Site
#from django.core.urlresolvers import reverse
from django.urls import reverse
import hashlib
import datetime as dt
from canchas.choices import *
from .paypal_impl import GetOrder, CaptureOrder
import mercadopago
import uuid

COMISION = 0.10

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                unique=True,
                                related_name='profile', on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField(blank=True, null=True, auto_now_add=False, auto_now=False)
    cod_tel = models.CharField(max_length=10, blank=True, null=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)

    def profile_image_url(self):
        fb_uid = SocialAccount.objects.filter(user_id=self.user.id, provider='facebook')

        if len(fb_uid):
            return "https://graph.facebook.com/{}/picture?width=40&height=40".format(fb_uid[0].uid)

        return "https://www.gravatar.com/avatar/{}?s=40".format(hashlib.md5(self.user.email).hexdigest())

    def __unicode__(self):
        return str(self.user.id) + self.nombre + self.apellido


class OwnerEstablecimiento(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                unique=True,
                                related_name='dueno', on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField(blank=True, null=True, auto_now_add=False, auto_now=False)

    def __str__(self):
        return str(self.user.id) + str(self.nombre) + str(self.apellido)


class EmpleadoEstablecimiento(models.Model):
    empleador = models.ForeignKey(OwnerEstablecimiento, on_delete=models.CASCADE, related_name='empleados')
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                unique=True,
                                related_name='empleado', on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)

    def __str__(self):
        return str(self.nombre) + str(self.apellido)


class Establecimiento(models.Model):
    owner = models.ForeignKey(OwnerEstablecimiento, on_delete=models.CASCADE, related_name='establecimientos')
    nombre = models.CharField(max_length=100)
    pais = models.CharField(default='ARG', max_length=100, 
        choices=PAISES_CHOICES)
    provincia = models.CharField(default='', max_length=100)
    localidad = models.CharField(default='', max_length=100)
    direccion = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True, max_length=500)
    vestuario = models.BooleanField(default=False)
    asador = models.BooleanField(default=False)
    estacionamiento = models.BooleanField(default=False)
    duchas = models.BooleanField(default=False)
    direccion_lat = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    direccion_lng = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)

    def __str__(self):
        return str(self.nombre)

class Facturacion(models.Model):
    establecimiento = models.OneToOneField(Establecimiento,
                                unique=True,
                                related_name='facturacion', on_delete=models.CASCADE)
    metodo_de_pago = models.CharField(max_length=100, blank=True, null=True, choices=FACTURACION)
    cbu = models.CharField(max_length=22, blank=True, null=True)
    mercadopago = models.CharField(max_length=100, blank=True, null=True)

class Images(models.Model):
    establecimiento = models.ForeignKey(Establecimiento, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='establecimientos/',
                              verbose_name='Image', blank=True, null=True)

    def __str__(self):
        return str(self.establecimiento.nombre) + "Image"


class Cancha(models.Model):
    establecimiento = models.ForeignKey(Establecimiento, on_delete=models.CASCADE, related_name="canchas", blank=True, null=True)
    nombre = models.CharField(max_length=100, blank=True, null=True) 
    deporte = models.CharField(max_length=100, blank=True, null=True, choices=DEPORTE)
    superficie = models.CharField(max_length=100, blank=True, null=True)
    techada = models.BooleanField(default=False)
    luz = models.BooleanField(default=False)
    comision = models.DecimalField(max_digits=9, decimal_places=2, default=COMISION)
    descripcion = models.TextField(blank=True, null=True, max_length=500)
    precio_sin_luz = models.IntegerField(default=0)
    precio_con_luz = models.IntegerField(default=0, blank=True, null=True)
    lunes = models.BooleanField(default=False)
    lunes_doble_turno = models.BooleanField(default=False)
    desde_lunes = models.TimeField(blank=True, null=True)
    hasta_lunes = models.TimeField(blank=True, null=True)
    desde_lunes_tarde = models.TimeField(blank=True, null=True)
    hasta_lunes_tarde = models.TimeField(blank=True, null=True)
    martes = models.BooleanField(default=False)
    martes_doble_turno = models.BooleanField(default=False)
    desde_martes = models.TimeField(blank=True, null=True)
    hasta_martes = models.TimeField(blank=True, null=True)
    desde_martes_tarde = models.TimeField(blank=True, null=True)
    hasta_martes_tarde = models.TimeField(blank=True, null=True)
    miercoles = models.BooleanField(default=False)
    miercoles_doble_turno = models.BooleanField(default=False)
    desde_miercoles = models.TimeField(blank=True, null=True)
    hasta_miercoles = models.TimeField(blank=True, null=True)
    desde_miercoles_tarde = models.TimeField(blank=True, null=True)
    hasta_miercoles_tarde = models.TimeField(blank=True, null=True)
    jueves = models.BooleanField(default=False)
    jueves_doble_turno = models.BooleanField(default=False)
    desde_jueves = models.TimeField(blank=True, null=True)
    hasta_jueves = models.TimeField(blank=True, null=True)
    desde_jueves_tarde = models.TimeField(blank=True, null=True)
    hasta_jueves_tarde = models.TimeField(blank=True, null=True)
    viernes = models.BooleanField(default=False)
    viernes_doble_turno = models.BooleanField(default=False)
    desde_viernes = models.TimeField(blank=True, null=True)
    hasta_viernes = models.TimeField(blank=True, null=True)
    desde_viernes_tarde = models.TimeField(blank=True, null=True)
    hasta_viernes_tarde = models.TimeField(blank=True, null=True)
    sabado = models.BooleanField(default=False)
    sabado_doble_turno = models.BooleanField(default=False)
    desde_sabado = models.TimeField(blank=True, null=True)
    hasta_sabado = models.TimeField(blank=True, null=True)
    desde_sabado_tarde = models.TimeField(blank=True, null=True)
    hasta_sabado_tarde = models.TimeField(blank=True, null=True)
    domingo = models.BooleanField(default=False)
    domingo_doble_turno = models.BooleanField(default=False)    
    desde_domingo = models.TimeField(blank=True, null=True)
    hasta_domingo = models.TimeField(blank=True, null=True)
    desde_domingo_tarde = models.TimeField(blank=True, null=True)
    hasta_domingo_tarde = models.TimeField(blank=True, null=True)

    def __str__(self):
        return "cancha de " + str(self.establecimiento.nombre) + str(self.deporte)


class ImagesCancha(models.Model):
    cancha = models.ForeignKey(Cancha, on_delete=models.SET_NULL, default=None, null=True)
    image = models.ImageField(upload_to='canchas/',
                              verbose_name='Image', blank=True, null=True)

    def __str__(self):
        return str(self.cancha.deporte) + " " + str(self.id)


class Reserva(models.Model):
    creador_de_reserva = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, related_name="reservas", blank=True, null=True)
    cancha = models.ForeignKey(Cancha, on_delete=models.SET_NULL, related_name='reservas', blank=True, null=True)
    confirmada = models.BooleanField(default=False)
    cancelada = models.BooleanField(default=False)
    pendiente = models.BooleanField(default=True)
    fecha = models.DateField(blank=True, null=True, auto_now_add=False, auto_now=False)
    #horario_inicio = models.TimeField(blank=True, null=True)
    #horario_fin = models.TimeField(blank=True, null=True)
    periodo = models.CharField(max_length=50, choices=TIME_CHOICES, null=True)
    con_luz = models.BooleanField(default=False)
    asistio = models.BooleanField(default=False)
    mp_id = models.CharField(verbose_name=u'ID Transacción de Mercadopago', max_length=100, null=True, blank=True)
    mp_pendiente = models.BooleanField(default=False)
    mp_url = models.CharField(verbose_name='Dirección p/Pago', max_length=255, default='', help_text='Puede copiar esta dirección para enviar por email u otro medio')
    uuid = models.CharField(max_length=8, null=True, editable=False)
    estado = models.CharField(max_length=50, choices=ESTADOS, default='pendiente')
    deposito_reserva = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    saldo = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    cancelada_por_cliente = models.BooleanField(default=False, blank=True)
    retiro = models.CharField(max_length=20, choices=RETIRO_ESTADO, default='A liquidar')
    codigo_operacion = models.CharField('Código operación', max_length=20, null=True)

    def __str__(self):
        if self.creador_de_reserva and self.cancha:
            return "reserva " + str(self.creador_de_reserva.id) + " " + str(self.cancha.id)
        else:
            return "reserva"

    def save(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = str(uuid.uuid1()).split('-')[0]
        super(Reserva, self).save(*args, **kwargs)

    def costo_deposito(self):
        # Porcentaje Comision MisCanchas

        deposito = 0.0
        #fin = datetime.datetime.combine(datetime.date.today(), self.horario_fin)
        #inicio = datetime.datetime.combine(datetime.date.today(), self.horario_inicio)

        # tiempo = (fin - inicio).total_seconds() / 3600 #EN HORAS
        deposito = self.cancha.precio_sin_luz * COMISION * 1
        #deposito = self.cancha.precio_sin_luz * COMISION * tiempo

        if self.con_luz:
            print('Precio cancha con luz ', self.cancha.precio_con_luz)
            deposito = self.cancha.precio_con_luz * COMISION * 1
            # deposito = self.cancha.precio_con_luz * COMISION * tiempo
        print("precio deposito ",deposito)
        print(30*'*')
        return deposito

    def calcular_saldo(self):
        saldo = 0.0
        deposito = self.costo_deposito()
        # fin = datetime.datetime.combine(datetime.date.today(), self.horario_fin)
        # inicio = datetime.datetime.combine(datetime.date.today(), self.horario_inicio)

        # tiempo = (fin - inicio).total_seconds() / 3600 # En horas
        if self.con_luz:
            print('Precio cancha con luz ',self.cancha.precio_con_luz)
            saldo = (self.cancha.precio_con_luz * 1) - deposito
            # saldo = (self.cancha.precio_con_luz * tiempo) - deposito
        else:
            saldo = (self.cancha.precio_sin_luz * 1) - deposito
            # saldo = (self.cancha.precio_sin_luz * tiempo) - deposito
            print('Precio cancha sin luz ',self.cancha.precio_sin_luz)
        return saldo


    def generar_cupon_mercadopago(self):
        """configura la reserva para ser pagada via mercadopago"""

        site = Site.objects.get_current()
        mp = mercadopago.MP(settings.MP_CLIENT_ID, settings.MP_CLIENT_SECRET)

        if self.mp_id and self.mp_pendiente:
            # TODO Log this.
            mp.cancel_payment(self.mp_id)

        # nuevo id
        self.mp_id = str(uuid.uuid1())

        title = "Mis Canchas {}: dia {} de {} ".format(self.cancha.nombre,
                                                         self.fecha.strftime("%d/%m/%Y"),
                                                         self.periodo)

        preference = mp.create_preference({
            "items": [
                {
                    "id": str(self.id),
                    "title": title,
                    "quantity": 1,
                    "currency_id": "ARS",
                    "unit_price": float(self.costo_deposito())
                }
            ],
            "payer": {
                "name": str(self.creador_de_reserva.nombre) + '' + str(self.creador_de_reserva.apellido),
                "email": str(self.creador_de_reserva.user.email),
            },
            "back_urls": {
                #"success": 'http://127.0.0.1:8000' + reverse('gracias_mp')
                "success": 'https://miscanchas.com' + reverse('gracias_mp')
                #"success": "http://142.93.49.186:8000"+reverse('reservas_list_fe'),
            },
            "auto_return": "approved",
            "external_reference": self.mp_id,
            "notification_url": 'https://miscanchas.com' + reverse('ipn'),
            #"notification_url": site.domain + reverse('ipn'),
        })

        print('PREFERENCES')
        print(preference['response'])
        #print(preference['notification_url'])

        if settings.MP_SANDBOX_MODE:
            url = preference['response']['sandbox_init_point']
        else:
            
            url = preference['response']['init_point']
        self.mp_url = url
        self.deposito_reserva = float(self.costo_deposito())
        self.save(update_fields=['mp_id', 'mp_url', 'deposito_reserva'])

    def is_paypal_reserva_pago(self, request_body):
        data = json.loads(request_body)
        order_id = data['orderID']
        
        # detalle = GetOrder(movimiento).get_order(order_id)
        detalle = GetOrder().get_order(order_id)
        detalle_precio = float(detalle.result.purchase_units[0].amount.value)

        # if float(detalle_precio) == float(movimiento.importe):
        transaccion = CaptureOrder().capture_order(order_id, debug=False)

        if (
            transaccion.status_code in [200, 201] and 
            transaccion.result.purchase_units[0].payments.captures[0].status in ['APPROVED', 'COMPLETED']
        ):
            print(f'''
                PAGO REALIZADO CON ÉXITO:
                Código operación: {transaccion.result.purchase_units[0].reference_id}
                Status Code:, {transaccion.status_code}
                Status: {transaccion.result.status}
                Order ID:, {transaccion.result.id}
                '''
            )
            return True
        else:
            print(f'''
                ERROR AL COMPLETAR EL PAGO
                Código operación: {transaccion.result.purchase_units[0].reference_id}
                Status Code: {transaccion.status_code}
                Status: {transaccion.result.status}
                Order ID: {transaccion.result.id}
                '''
            )
            return False
        # else:
        #     print(f'''
        #         Código operación: {movimiento.codigo_operacion}
        #         Precios incorrectos:
        #         '''
        #     )
        #     return Movimiento.ESTADO_NO_FINALIZADA
    


class Favorito(models.Model):
    usuario = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, related_name='favoritos', blank=True, null=True)
    cancha = models.ForeignKey(Cancha, on_delete=models.SET_NULL, related_name='favoritos', blank=True, null=True)

    def __str__(self):
        return str(self.id)
