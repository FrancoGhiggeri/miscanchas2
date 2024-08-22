# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext as _

from django.contrib.auth import get_user_model
from canchas.models import *

from django.contrib.auth.forms import UserCreationForm

from django.utils.text import capfirst
from django.core.files.images import get_image_dimensions
from django.forms import modelformset_factory
from canchas.choices import *
import floppyforms as fforms

time_widget = forms.widgets.TimeInput(attrs={'class': 'time-pick'})
valid_time_formats = ['%H:%M', '%I:%M%p', '%I:%M %p']

class ContactForm(fforms.Form):

    nombre = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    asunto = forms.CharField(required=True)
    mensaje = forms.CharField(widget=forms.Textarea)


class UserProfileForm(forms.ModelForm):
    fecha_nacimiento = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS, required=False)

    class Meta:
        model = UserProfile
        fields = ['nombre', 'apellido', 'fecha_nacimiento']


class OwnerEstablecimientoForm(forms.ModelForm):

    class Meta:
        model = OwnerEstablecimiento
        fields = ['nombre', 'apellido']


class FacturacionForm(forms.ModelForm):
    class Meta:
        model = Facturacion
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        if hasattr(self.user, 'empleado'):
            establecimientos = Establecimiento.objects.filter(
                owner=self.user.empleado.empleador)
        else:
            establecimientos = Establecimiento.objects.filter(
                owner=self.user.dueno)

        self.fields['establecimiento'].queryset = establecimientos


class EmpleadoEstablecimientoForm(forms.ModelForm):

    class Meta:
        model = EmpleadoEstablecimiento
        fields = ['nombre', 'apellido']


class UserForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['email', 'password']


class EstablecimientoForm(forms.ModelForm):
    class Meta:
        model = Establecimiento
        exclude = ['owner']


class CanchaForm(forms.ModelForm):
    class Meta:
        model = Cancha
    #    fields = "__all__"
        exclude = ['establecimiento', 'comision']
        widgets = {'desde_lunes': forms.Select(choices=HOUR_CHOICES),
                   'hasta_lunes': forms.Select(choices=HOUR_CHOICES),
                   'desde_lunes_tarde': forms.Select(choices=HOUR_CHOICES),
                   'hasta_lunes_tarde': forms.Select(choices=HOUR_CHOICES),
                   'desde_martes': forms.Select(choices=HOUR_CHOICES),
                   'hasta_martes': forms.Select(choices=HOUR_CHOICES),
                   'desde_martes_tarde': forms.Select(choices=HOUR_CHOICES),
                   'hasta_martes_tarde': forms.Select(choices=HOUR_CHOICES),
                   'desde_miercoles': forms.Select(choices=HOUR_CHOICES),
                   'hasta_miercoles': forms.Select(choices=HOUR_CHOICES),
                   'desde_miercoles_tarde': forms.Select(choices=HOUR_CHOICES),
                   'hasta_miercoles_tarde': forms.Select(choices=HOUR_CHOICES),
                   'desde_jueves': forms.Select(choices=HOUR_CHOICES),
                   'hasta_jueves': forms.Select(choices=HOUR_CHOICES),
                   'desde_jueves_tarde': forms.Select(choices=HOUR_CHOICES),
                   'hasta_jueves_tarde': forms.Select(choices=HOUR_CHOICES),
                   'desde_viernes': forms.Select(choices=HOUR_CHOICES),
                   'hasta_viernes': forms.Select(choices=HOUR_CHOICES),
                   'desde_viernes_tarde': forms.Select(choices=HOUR_CHOICES),
                   'hasta_viernes_tarde': forms.Select(choices=HOUR_CHOICES),
                   'desde_sabado': forms.Select(choices=HOUR_CHOICES),
                   'hasta_sabado': forms.Select(choices=HOUR_CHOICES),
                   'desde_sabado_tarde': forms.Select(choices=HOUR_CHOICES),
                   'hasta_sabado_tarde': forms.Select(choices=HOUR_CHOICES),
                   'desde_domingo': forms.Select(choices=HOUR_CHOICES),
                   'hasta_domingo': forms.Select(choices=HOUR_CHOICES),
                   'desde_domingo_tarde': forms.Select(choices=HOUR_CHOICES),
                   'hasta_domingo_tarde': forms.Select(choices=HOUR_CHOICES)}


class CanchaFormBackoffice(forms.ModelForm):
    #desde_lunes = forms.TimeField(required=False, widget=time_widget, help_text='ex: 10:30AM', input_formats=valid_time_formats)
    
    class Meta:
        model = Cancha
        #fields = "__all__"
        exclude = ['comision']
        widgets = {'desde_lunes': forms.Select(choices=HOUR_CHOICES),
                   'hasta_lunes': forms.Select(choices=HOUR_CHOICES),
                   'desde_lunes_tarde': forms.Select(choices=HOUR_CHOICES),
                   'hasta_lunes_tarde': forms.Select(choices=HOUR_CHOICES),
                   'desde_martes': forms.Select(choices=HOUR_CHOICES),
                   'hasta_martes': forms.Select(choices=HOUR_CHOICES),
                   'desde_martes_tarde': forms.Select(choices=HOUR_CHOICES),
                   'hasta_martes_tarde': forms.Select(choices=HOUR_CHOICES),
                   'desde_miercoles': forms.Select(choices=HOUR_CHOICES),
                   'hasta_miercoles': forms.Select(choices=HOUR_CHOICES),
                   'desde_miercoles_tarde': forms.Select(choices=HOUR_CHOICES),
                   'hasta_miercoles_tarde': forms.Select(choices=HOUR_CHOICES),
                   'desde_jueves': forms.Select(choices=HOUR_CHOICES),
                   'hasta_jueves': forms.Select(choices=HOUR_CHOICES),
                   'desde_jueves_tarde': forms.Select(choices=HOUR_CHOICES),
                   'hasta_jueves_tarde': forms.Select(choices=HOUR_CHOICES),
                   'desde_viernes': forms.Select(choices=HOUR_CHOICES),
                   'hasta_viernes': forms.Select(choices=HOUR_CHOICES),
                   'desde_viernes_tarde': forms.Select(choices=HOUR_CHOICES),
                   'hasta_viernes_tarde': forms.Select(choices=HOUR_CHOICES),
                   'desde_sabado': forms.Select(choices=HOUR_CHOICES),
                   'hasta_sabado': forms.Select(choices=HOUR_CHOICES),
                   'desde_sabado_tarde': forms.Select(choices=HOUR_CHOICES),
                   'hasta_sabado_tarde': forms.Select(choices=HOUR_CHOICES),
                   'desde_domingo': forms.Select(choices=HOUR_CHOICES),
                   'hasta_domingo': forms.Select(choices=HOUR_CHOICES),
                   'desde_domingo_tarde': forms.Select(choices=HOUR_CHOICES),
                   'hasta_domingo_tarde': forms.Select(choices=HOUR_CHOICES)}

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', '')
        super(CanchaFormBackoffice, self).__init__(*args, **kwargs)

        if hasattr(user, 'dueno'):
            self.fields['establecimiento'] = forms.ModelChoiceField(
                queryset=Establecimiento.objects.filter(owner=user.dueno))
        if hasattr(user, 'empleado'):
            self.fields['establecimiento'] = forms.ModelChoiceField(
                queryset=Establecimiento.objects.filter(
                    owner=user.empleado.empleador))

class ReservaFormAsistencia(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['asistio',]


class EmpleadoEstablecimientoForm(forms.ModelForm):
    class Meta:
        model = EmpleadoEstablecimiento
        exclude = ['empleador', 'user']


class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        exclude = ['creador_de_reserva', 'cancha', 'confirmada', 'cancelada',
                   'pendiente', 'asistio', 'mp_id', 'mp_pendiente', 'mp_url',
                   'uuid', 'estado', 'deposito_reserva', 'cancelada_por_cliente',
                   'retiro', 'saldo']


class CancelacionForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['retiro']


class ImageForm(forms.ModelForm):

    class Meta:
        model = Images
        fields = ('image', )

ImageFormSet = modelformset_factory(Images, form=ImageForm, extra=3)
ImagesCanchaFormSet = modelformset_factory(ImagesCancha, form=ImageForm, extra=3)