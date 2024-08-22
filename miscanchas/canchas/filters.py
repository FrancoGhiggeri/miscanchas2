# -*- coding: utf-8 -*-
import django_filters

from canchas.models import *
from canchas.choices import *


class EstablecimientoFilter(django_filters.FilterSet):
    nombre = django_filters.CharFilter(label='Nombre', lookup_expr='icontains')
    direccion = django_filters.CharFilter(label='Direccion', lookup_expr='icontains')
    canchas__deporte = django_filters.ChoiceFilter(label='Deportes', choices=DEPORTE)
    techada = django_filters.BooleanFilter(label='Techada')
    vestuario = django_filters.BooleanFilter(label='Vestuario')
    estacionamiento = django_filters.BooleanFilter(label='Estacionamiento')
    asador = django_filters.BooleanFilter(label='Asador')
    pais = django_filters.ChoiceFilter(label='Pais', choices='PAISES_CHOICES')
    provincia = django_filters.CharFilter(label='Provincia', lookup_expr='icontains')
    localidad = django_filters.CharFilter(label='Localidad', lookup_expr='icontains')
    canchas__superficie = django_filters.ChoiceFilter(label='Superficie', lookup_expr='icontains')



    class Meta:
        model = Establecimiento
        fields = ['nombre', 'direccion', 'canchas__deporte', 'techada', 'canchas__superficie',
                  'vestuario', 'estacionamiento', 'asador', 'pais', 'provincia', 'localidad']


class CanchaFilter(django_filters.FilterSet):
    establecimiento__nombre = django_filters.CharFilter(label='Nombre del Establecimiento', lookup_expr='icontains')
    # establecimiento__direccion = django_filters.CharFilter(label='direccion', lookup_expr='icontains')
    # establecimiento__pais = django_filters.ChoiceFilter(label='Pais', choices=PAISES_CHOICES)
    establecimiento__provincia = django_filters.CharFilter(label='Provincia', lookup_expr='icontains')
    establecimiento__localidad = django_filters.CharFilter(label='Localidad', lookup_expr='icontains')
    establecimiento__vestuario = django_filters.BooleanFilter(label='Vestuario')
    establecimiento__estacionamiento = django_filters.BooleanFilter(label='Estacionamiento')
    establecimiento__asador = django_filters.BooleanFilter(label='Asador')

    # nombre = django_filters.CharFilter(label='Nombre', lookup_expr='icontains')
    superficie = django_filters.ChoiceFilter(label='Superficie', lookup_expr='icontains', choices=SUPERFICIE)
    deporte = django_filters.ChoiceFilter(label='Deporte', choices=DEPORTE)
    techada = django_filters.BooleanFilter(label='Techada')
    luz = django_filters.BooleanFilter(label='Luz')

    class Meta:
        model = Cancha
        fields = [
            'establecimiento__nombre',
            'establecimiento__localidad',
            'establecimiento__provincia',
            'deporte',
            'superficie',
            'techada',
            'luz',
            'establecimiento__vestuario',
            'establecimiento__estacionamiento',
            'establecimiento__asador'
        ]


class FrontendBusquedaFilter(django_filters.FilterSet):
    deporte = django_filters.ChoiceFilter(label='Deporte', choices=DEPORTE)
    superficie = django_filters.ChoiceFilter(label='Superficie', lookup_expr='icontains', choices=DEPORTE)
    establecimiento__provincia = django_filters.CharFilter(label='Provincia', lookup_expr='icontains')
    establecimiento__localidad = django_filters.CharFilter(label='Localidad', lookup_expr='icontains')

    class Meta:
        model = Cancha
        fields = [
            'establecimiento__localidad',
            'establecimiento__provincia',
            'deporte',
            'superficie'
        ]
