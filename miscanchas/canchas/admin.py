from django.contrib import admin
from canchas.models import *
# Register your models here.

from django.contrib.sites.models import Site

class EstablecimientoAdmin(admin.ModelAdmin):
    pass

admin.site.register(Establecimiento, EstablecimientoAdmin)


class CanchaAdmin(admin.ModelAdmin):
    pass

admin.site.register(Cancha, CanchaAdmin)


class ReservaAdmin(admin.ModelAdmin):
    pass

admin.site.register(Reserva, ReservaAdmin)


admin.site.register(UserProfile)
admin.site.register(OwnerEstablecimiento)

admin.site.register(Images)
admin.site.register(ImagesCancha)
admin.site.register(Favorito)
admin.site.register(EmpleadoEstablecimiento)