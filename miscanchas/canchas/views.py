from django.shortcuts import render, get_object_or_404
from django.contrib.auth import logout, authenticate, login
from django.template import RequestContext, loader
from custom_user.forms import EmailUserCreationForm, EmailUserChangeForm
from django.views.decorators.cache import never_cache
from django.views.generic.edit import UpdateView, DeleteView, CreateView, FormMixin, FormView
from django.views.generic.detail import DetailView
from django.http import Http404
from django.views.generic.list import ListView
#from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.urls import reverse
# from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers
from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.db.models import Q
from django.forms.models import model_to_dict
from django.conf import settings
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from canchas.models import *
from canchas.forms import *
from canchas.filters import *
from canchas.choices import *
from datetime import datetime 
from django.views.decorators.csrf import csrf_exempt
import json
from collections import OrderedDict
from decouple import config

import mercadopago

from canchas.utils import generate_unique_code


DATES = {'1': 'lunes', '2': 'martes', '3': 'miercoles', '4': 'jueves', '5': 'viernes', '6':'sabado', '7':'domingo'}
HOUR_OF_DAY_24 = [(i, j) for i in range(00, 24) for j in [00, 30]]


def f(i):
    return str(i) + ':00Hs a ' + str(i + 1) + ':00Hs'
PERIOD_HOUR = [(f(i), f(i)) for i in range(0, 24)]


def disponibilidad_cancha(request, year, month, day, establecimiento_id, cancha_id):
    plain = []
    cancha = Cancha.objects.get(id=cancha_id)
    data = {el[0]: False for el in PERIOD_HOUR}

    schedule = OrderedDict(data.items())
    bookings = OrderedDict(data.items())

    cancels = OrderedDict(data.items())

    date = str(day) + '/' + str(month) + '/' + str(year)
    fecha = datetime.strptime(date, '%d/%m/%Y').date()
    reservas = Reserva.objects.filter(cancha=cancha, fecha=fecha, estado='acreditada', cancelada_por_cliente=False)
    reservas_canceladas_cliente = Reserva.objects.filter(cancha=cancha, fecha=fecha, cancelada_por_cliente=True)

    dia_de_la_semana_numero = fecha.isoweekday()
    if dia_de_la_semana_numero == 1:
        hora_inicio = cancha.desde_lunes.hour
        hora_fin = cancha.hasta_lunes.hour

        for idx, item in enumerate(schedule.items()):
            if hora_inicio <= idx <= hora_fin - 1:
                schedule[item[0]] = True

        #CHEQUEO Doble turno
        if cancha.lunes_doble_turno:
            hora_inicio2 = cancha.desde_lunes_tarde.hour
            hora_fin2 = cancha.hasta_lunes_tarde.hour

            for idx, item in enumerate(schedule.items()):
                if hora_inicio2 <= idx <= hora_fin2 - 1:
                    schedule[item[0]] = True

    elif dia_de_la_semana_numero == 2:
        hora_inicio = cancha.desde_martes.hour
        hora_fin = cancha.hasta_martes.hour

        for idx, item in enumerate(schedule.items()):
            if hora_inicio <= idx <= hora_fin - 1:
                schedule[item[0]] = True

        # CHEQUEO Doble turno
        if cancha.lunes_doble_turno:
            hora_inicio2 = cancha.desde_martes_tarde.hour
            hora_fin2 = cancha.hasta_martes_tarde.hour

            for idx, item in enumerate(schedule.items()):
                if hora_inicio2 <= idx <= hora_fin2 - 1:
                    schedule[item[0]] = True

    elif dia_de_la_semana_numero == 3:
        hora_inicio = cancha.desde_miercoles.hour
        hora_fin = cancha.hasta_miercoles.hour

        for idx, item in enumerate(schedule.items()):
            if hora_inicio <= idx <= hora_fin - 1:
                schedule[item[0]] = True

        # CHEQUEO Doble turno
        if cancha.lunes_doble_turno:
            hora_inicio2 = cancha.desde_miercoles_tarde.hour
            hora_fin2 = cancha.hasta_miercoles_tarde.hour

            for idx, item in enumerate(schedule.items()):
                if hora_inicio2 <= idx <= hora_fin2 - 1:
                    schedule[item[0]] = True

    elif dia_de_la_semana_numero == 4:
        hora_inicio = cancha.desde_jueves.hour
        hora_fin = cancha.hasta_jueves.hour

        for idx, item in enumerate(schedule.items()):
            if hora_inicio <= idx <= hora_fin - 1:
                schedule[item[0]] = True

        # CHEQUEO Doble turno
        if cancha.lunes_doble_turno:
            hora_inicio2 = cancha.desde_jueves_tarde.hour
            hora_fin2 = cancha.hasta_jueves_tarde.hour

            for idx, item in enumerate(schedule.items()):
                if hora_inicio2 <= idx <= hora_fin2 - 1:
                    schedule[item[0]] = True

    elif dia_de_la_semana_numero == 5:
        hora_inicio = cancha.desde_viernes.hour
        hora_fin = cancha.hasta_viernes.hour

        for idx, item in enumerate(schedule.items()):
            if hora_inicio <= idx <= hora_fin - 1:
                schedule[item[0]] = True

        # CHEQUEO Doble turno
        if cancha.lunes_doble_turno:
            hora_inicio2 = cancha.desde_viernes_tarde.hour
            hora_fin2 = cancha.hasta_viernes_tarde.hour

            for idx, item in enumerate(schedule.items()):
                if hora_inicio2 <= idx <= hora_fin2 - 1:
                    schedule[item[0]] = True

    elif dia_de_la_semana_numero == 6:
        hora_inicio = cancha.desde_sabado.hour
        hora_fin = cancha.hasta_sabado.hour

        for idx, item in enumerate(schedule.items()):
            if hora_inicio <= idx <= hora_fin - 1:
                schedule[item[0]] = True

        #CHEQUEO Doble turno
        if cancha.lunes_doble_turno:
            hora_inicio2 = cancha.desde_sabado_tarde.hour
            hora_fin2 = cancha.hasta_sabado_tarde.hour

            for idx, item in enumerate(schedule.items()):
                if hora_inicio2 <= idx <= hora_fin2 - 1:
                    schedule[item[0]] = True

    elif dia_de_la_semana_numero == 7:
        hora_inicio = cancha.desde_domingo.hour
        hora_fin = cancha.hasta_domingo.hour

        for idx, item in enumerate(schedule.items()):
            if hora_inicio <= idx <= hora_fin - 1:
                schedule[item[0]] = True

        # CHEQUEO Doble turno
        if cancha.lunes_doble_turno:
            hora_inicio2 = cancha.desde_domingo_tarde.hour
            hora_fin2 = cancha.hasta_domingo_tarde.hour

            for idx, item in enumerate(schedule.items()):
                if hora_inicio2 <= idx <= hora_fin2 - 1:
                    schedule[item[0]] = True

    for reserva in reservas:
        # marco los horarios que la cancha esta reservada
        bookings[reserva.periodo] = True

    for cancel in reservas_canceladas_cliente:
        cancels[cancel.periodo] = True

    for idx, item in enumerate(schedule.items()):
        result = OrderedDict()
        result['time'] = item[0]
        # add opening hours
        if schedule[item[0]]:
            # disponible
            result['status'] = 'available'
        else:
            # horario de cancha cerrada
            result['status'] = 'not-available'
        # remove cancelled bookings
        if cancels[item[0]]:
            result['status'] = 'available'
        # remove bookings
        if bookings[item[0]]:
            # reservado
            result['status'] = 'disabled'
        plain.append(result)
    print(plain)
    plain = sorted(plain, key= lambda x: datetime.strptime(x['time'].split('Hs')[0], '%H:%M'))

    app_json = json.dumps(plain)
    
    return HttpResponse(app_json, content_type='json')


def login_success(request):
    """
    Redirects users based on whether they are in the admins group
    """
    if hasattr(request.user, 'dueno') or hasattr(request.user, 'empleado'):
        return redirect("home_backoffice")
    else:
        return redirect("home")


class HomePageView(TemplateView):

    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context['establecimientos'] = Establecimiento.objects.all()
        return context


class HomePageBackofficeView(TemplateView):
    template_name = "home_backoffice.html"

    # Definir que mostrar en esta vista
    def get_context_data(self, **kwargs):
        context = super(HomePageBackofficeView, self).get_context_data(**kwargs)
        context['canchas'] = Cancha.objects.all()
        return context


def create_establecimiento(request):

    ImageFormSet = modelformset_factory(Images, fields=('image',), extra=3, max_num=3)

    if request.method == 'POST':

        establecimientoForm = EstablecimientoForm(request.POST)
        formset = ImageFormSet(request.POST or None, request.FILES or None, queryset=Images.objects.none())

        if establecimientoForm.is_valid() and formset.is_valid():
            establecimiento_form = establecimientoForm.save(commit=False)
            establecimiento_form.owner = request.user.dueno
            establecimiento_form.save()

            for form in formset.cleaned_data:
                image = form.get('image')
                photo = Images(establecimiento=establecimiento_form, image=image)
                photo.save()
            return redirect("cancha_create_backoffice")#, establecimiento_id=establecimiento_form.id)
        else:
            pass

    else:
        establecimientoForm = EstablecimientoForm()
        formset = ImageFormSet(queryset=Images.objects.none())
    return render(request, 'establecimiento/establecimiento_new.html',
                  {'establecimientoForm': establecimientoForm, 'formset': formset})


def update_establecimiento(request, pk):
    establecimiento = get_object_or_404(Establecimiento, id=pk)
    ImageFormSet = modelformset_factory(Images, fields=('image',), extra=3, max_num=3)
    if request.method == 'POST':
        establecimientoForm = EstablecimientoForm(request.POST or None, instance=establecimiento)
        formset = ImageFormSet(request.POST or None, request.FILES or None)
        if establecimientoForm.is_valid() and formset.is_valid():
            establecimientoForm.save()

            for index, f in enumerate(formset):
                if f.cleaned_data:

                    if f.cleaned_data['id'] is None:
                        photo = Images(establecimiento=establecimiento,
                                       image=f.cleaned_data.get('image'))
                        photo.save()
                    elif f.cleaned_data['image'] is False:
                        photo_del = Images(id=request.POST.get(
                            'form-' + str(index) + '-id'))
                        photo_del.delete()
                    else:
                        photo = Images(establecimiento=establecimiento, id=f.cleaned_data['id'].id)
                        new = Images(establecimiento=establecimiento, image=f.cleaned_data.get('image'))
                        photo.image = new.image
                        photo.save()

            return redirect('establecimiento_list')
    else:
        establecimientoForm = EstablecimientoForm(instance=establecimiento)
        formset = ImageFormSet(queryset=Images.objects.filter(establecimiento=establecimiento))

    return render(
        request, 'establecimiento/establecimiento_update.html',
        {'establecimientoForm': establecimientoForm, 'formset': formset})


def create_cancha(request, establecimiento_id):
    ImageFormSet = modelformset_factory(Images, fields=('image',), extra=3)

    if request.method == 'POST':
        canchaForm = CanchaForm(request.POST)
        formset = ImageFormSet(request.POST, request.FILES,
                               queryset=Images.objects.none())

        if canchaForm.is_valid() and formset.is_valid():
            cancha_form = canchaForm.save(commit=False)
            cancha_form.establecimiento = Establecimiento.objects.get(id=establecimiento_id)
            cancha_form.save()

            for form in formset.cleaned_data:
                image = form.get('image')
                photo = ImagesCancha(cancha=cancha_form, image=image)
                photo.save()
            return redirect("cancha_list", establecimiento_id=establecimiento_id)
        else:
            pass
    else:
        canchaForm = CanchaForm()
        formset = ImageFormSet(queryset=Images.objects.none())
    return render(request, 'cancha/cancha_new.html',
                  {'canchaForm': canchaForm, 'formset': formset})


def create_cancha_backoffice(request):
    ImageFormSet = modelformset_factory(Images, fields=('image',), extra=3)
    if request.method == 'POST':

        canchaForm = CanchaFormBackoffice(request.POST, user=request.user)
        formset = ImageFormSet(request.POST, request.FILES,
                               queryset=Images.objects.none())

        if canchaForm.is_valid() and formset.is_valid():
            cancha_form = canchaForm.save(commit=False)
            # just in case in future we want to manange another fields
            cancha_form.save()

            for form in formset.cleaned_data:
                image = form.get('image')
                photo = ImagesCancha(cancha=cancha_form, image=image)
                photo.save()
            return redirect("cancha_list", establecimiento_id=cancha_form.establecimiento.id)
        else:
            pass
    else:
        canchaForm = CanchaFormBackoffice(user=request.user)
        formset = ImageFormSet(queryset=Images.objects.none())
    return render(request, 'cancha/cancha_new_backoffice.html',
                  {'canchaForm': canchaForm, 'formset': formset})


def update_cancha(request, establecimiento_id, pk):
    cancha = get_object_or_404(Cancha, id=pk)
    ImageFormSet = modelformset_factory(ImagesCancha, fields=('image',), extra=3, max_num=3)
    if request.method == 'POST':
        canchaForm = CanchaForm(request.POST or None, instance=cancha)
        formset = ImageFormSet(request.POST or None, request.FILES or None)
        if canchaForm.is_valid() and formset.is_valid():
            print("VALID")
            canchaForm.save()
            data = ImagesCancha.objects.filter(cancha=cancha)
            for index, f in enumerate(formset):
                if f.cleaned_data:
                    if f.cleaned_data['id'] is None:
                        photo = ImagesCancha(cancha=cancha, image=f.cleaned_data.get('image'))
                        photo.save()
                    elif f.cleaned_data['image'] is False:
                        photo_del = ImagesCancha(id=request.POST.get('form-'+str(index)+'-id'))
                        photo_del.delete()
                    else:
                        photo = ImagesCancha(cancha=cancha, id=f.cleaned_data['id'].id)
                        new = ImagesCancha(cancha=cancha, image=f.cleaned_data.get('image'))
                        photo.image = new.image
                        photo.save()

            return redirect('cancha_list_full_backoffice')
    else:
        print("ELSE")
        canchaForm = CanchaForm(instance=cancha)
        formset = ImageFormSet(queryset=ImagesCancha.objects.filter(cancha=cancha))

    return render(
        request, 'cancha/cancha_update.html',
        {'canchaForm': canchaForm, 'formset': formset})


def logout_and_login(request):
    """
    Metodo que muestra la confirmacion del deslogueo
    """
    logout(request)
    return redirect('home')


def new_account(request):
    """ Vista para crear un nuevo usuario"""

    template = loader.get_template('registration/register.html')
    if request.method == 'POST':
        
        form = EmailUserCreationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password2']
            user = get_user_model().objects.create_user(
                email=email, password=password
            )
            user.save()
            new_user = authenticate(email=email, password=password)

            login(request, new_user)

            return HttpResponseRedirect(reverse('create_profile'))
    else:

        form = EmailUserCreationForm()

    context = RequestContext(request, {
        'form': form,
    })
    return render(request, 'registration/register.html', {'form': form})


def edit_profile(request):
    template = loader.get_template('registration/profile_edit.html')

    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        return HttpResponse("invalid user_profile!")

    if request.method == 'POST':
        form = UpdateProfileForm(data=request.POST, instance=user_profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user

            if 'avatar' in request.FILES:
                profile.avatar = request.FILES['avatar']

            profile.save()

            return HttpResponseRedirect(reverse('home_backoffice'))
        else:
            pass
            

    else:
        user = request.user
        profile = user.profile
        form = UserProfileForm(instance=profile)
    return render(request, 'registration/profile_edit.html', {'fom': form})


def new_owner(request):
    """ Vista para crear un nuevo usuario admin"""
    if request.method == 'POST':
        form = EmailUserCreationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password2']
            user = get_user_model().objects.create_user(
                email=email, password=password
            )
            user.save()

            new_user = authenticate(email=email, password=password)
            login(request, new_user)
            return HttpResponseRedirect(reverse('create_profile_owner'))
    else:
        form = EmailUserCreationForm()

    context = {'form': form, }
    return render(request, 'owner/new_owner.html', context)


class OwnerProfileCreate(CreateView):
    model = OwnerEstablecimiento
    form_class = OwnerEstablecimientoForm
    template_name = 'owner/owner_profile_new.html'

    def get_success_url(self):
        return reverse('establecimiento_create')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(OwnerProfileCreate, self).form_valid(form)

    def dispatch(self, *args, **kwargs):
        return super(OwnerProfileCreate, self).dispatch(*args, **kwargs)


class UserProfileCreate(CreateView):
    model = UserProfile
    form_class = UserProfileForm
    template_name = 'registration/profile_new.html'

    def get_success_url(self):
        return reverse('home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(UserProfileCreate, self).form_valid(form)

    def dispatch(self, *args, **kwargs):
        return super(UserProfileCreate, self).dispatch(*args, **kwargs)
    
def create_user_profile(request):
    user = request.user

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        fecha_nacimiento = request.POST.get('fecha_nacimiento')
        role = request.POST.get('role')

        if role == 'jugador':
            UserProfile.objects.create(
                user=user, 
                nombre=nombre, 
                apellido=apellido, 
                fecha_nacimiento=fecha_nacimiento
            )
            return redirect(reverse('home'))
        elif role == 'dueno':
            OwnerEstablecimiento.objects.create(
                user=user,
                nombre=nombre,
                apellido=apellido,
                fecha_nacimiento=fecha_nacimiento
            )
            return redirect(reverse('establecimiento_create'))

    return render(request, 'registration/profile_new.html')


class EstablecimientoDetail(DetailView):
    model = Establecimiento
    form_class = EstablecimientoForm
    template_name = 'establecimiento/establecimiento_detail.html'

    def get_context_data(self, **kwargs):
        context = super(EstablecimientoDetail, self).get_context_data(**kwargs)
        context['canchas'] = Cancha.objects.all()
        return context


class EstablecimientoDetailFront(DetailView):
    model = Establecimiento
    form_class = EstablecimientoForm
    template_name = 'establecimiento/establecimiento_detail_public.html'

    def get_context_data(self, **kwargs):
        context = super(EstablecimientoDetailFront, self).get_context_data(**kwargs)
        context['canchas'] = Cancha.objects.filter(establecimiento=self.kwargs['pk'])
        return context


class EstablecimientoDelete(DeleteView):
    model = Establecimiento
    template_name = 'establecimiento/establecimiento_delete.html'

    def get_success_url(self): 
        return reverse('establecimiento_list')


class EstablecimientoList(ListView):
    model = Establecimiento
    template_name = 'establecimiento/establecimiento_list.html'

    def get_queryset(self):
        qs = super(EstablecimientoList, self).get_queryset()
        if hasattr(self.request.user, 'empleado'):
            qset = Establecimiento.objects.filter(
                owner=self.request.user.empleado.empleador)
        else:
            qset = Establecimiento.objects.filter(
                owner=self.request.user.dueno)
        return qset


class CanchaCreate(CreateView):
    model = Cancha
    form_class = CanchaForm
    template_name = 'cancha/cancha_new.html'

    def get_success_url(self): 
        return reverse('cancha_list')

    def form_valid(self, form):
        form.instance.creador = self.request.user

        return super(CanchaCreate, self).form_valid(form)


class CanchaDetail(DetailView):
    model = Cancha
    form_class = CanchaForm
    template_name = 'cancha/cancha_detail.html'


class CanchaDetailFront(DetailView):
    model = Cancha
    form_class = CanchaForm
    template_name = 'cancha/cancha_detail_public.html'


class CanchaUpdate(UpdateView):
    model = Cancha
    form_class = CanchaForm
    template_name = 'cancha/cancha_update.html'

    def get_success_url(self): 
        return reverse('cancha_list', kwargs={'establecimiento_id': self.kwargs['establecimiento_id']})


class CanchaDelete(DeleteView):
    model = Cancha
    template_name = 'cancha/cancha_delete.html'

    def get_success_url(self): 
        return reverse('cancha_list', kwargs={'establecimiento_id': self.kwargs['establecimiento_id']})


class CanchaList(ListView):
    model = Cancha
    template_name = 'cancha/cancha_list.html'

    def get_queryset(self):
        qs = super(CanchaList, self).get_queryset()
        # Retrieve only canchas from the establecimiento which is logged in
        establecimiento = Establecimiento.objects.get(id=self.kwargs['establecimiento_id'])
        return qs.filter(establecimiento=establecimiento)


class CanchaListFull(ListView):
    model = Cancha
    template_name = 'cancha/cancha_list_full.html'

    def get_queryset(self):
        qs = super(CanchaListFull, self).get_queryset()
        # Retrieve only canchas from the establecimiento which is logged in
        if hasattr(self.request.user, 'dueno'):
            qs = qs.filter(establecimiento__owner=self.request.user.dueno)
        elif hasattr(self.request.user, 'empleado'):
            qs = qs.filter(establecimiento__owner=self.request.user.empleado.empleador)
        return qs


def cancha_list(request, *args, **kwargs):
    cancha_list = Cancha.objects.all()
    cancha_filter = CanchaFilter(request.GET, queryset=cancha_list)
    return render(request, 'cancha/cancha_list.html', {'filter': cancha_filter})


def gracias_mp(request):
    print('session gracias mp')
    reserva_id = request.session.pop('reserva_reciente', None)
    reserva = Reserva.objects.get(id=reserva_id)
    reserva.estado = 'acreditada'
    reserva.save()
    site = Site.objects.get_current()

    mail_txt = render_to_string('mail_mp_txt.html', {'reserva': reserva})
    try:
        msg = EmailMultiAlternatives(
            u'Recibimos tu reserva %s - Mis Canchas /ref. #%s' % (site.name, reserva.id),
            mail_txt, 'no-reply@miscanchas.com', [reserva.creador_de_reserva.user.email],)
            #cc=['no-reply@miscanchas.com'])
        msg.send()
    except Exception as err:
        print(str(err))

    return render(request, 'gracias_mp.html', {'gracias': True, 'reserva': reserva})

def compra_finalizada(request):
    reserva = Reserva.objects.all().last()
    return render(request, 'gracias_mp.html', {'gracias': True, 'reserva': reserva})
    


def redirector(reserva, *args, **kwargs):
    reserva = Reserva.objects.get(id=kwargs['pk'])
    url = str(reserva.mp_url)
    return redirect(url)


class ReservaCreate(CreateView):
    model = Reserva
    form_class = ReservaForm
    template_name = 'reserva/reserva_new.html'

    def get_success_url(self):
        self.object.saldo = self.object.calcular_saldo()
        # medio_de_pago = self.request.POST.get('role')
        '''if medio_de_pago == 'mp':
            self.object.generar_cupon_mercadopago()
        elif medio_de_pago == 'paypal':
            self.object.genera'''
        self.request.session['reserva_reciente'] = self.object.id
        self.object.save()
        mail_txt = render_to_string('nueva_reserva_email_owner.html', {'reserva': self.object})

        try:
            msg = EmailMultiAlternatives(
                u' Has recibido una nueva reserva - Mis Canchas /ref. #%s' % (self.object.id),
                mail_txt, 'no-reply@miscanchas.com', [self.object.cancha.establecimiento.owner.user],)
            msg.send()
        except Exception as err:
            print(str(err))

        return reverse('redirector', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        context = super(ReservaCreate, self).get_context_data(**kwargs)
        cancha = Cancha.objects.get(id=self.kwargs['pk'])
        context['cancha'] = cancha
        context['ya_reservado'] = cancha.reservas.filter(confirmada=True)
        context['paypal_client_id'] = config('PAYPAL_CLIENT_ID')
        context['paypal_secret_key'] = config('PAYPAL_SECRET_KEY')
        context['codigo_operacion'] = generate_unique_code()
        return context

    def form_valid(self, form):
        user_profile = UserProfile.objects.filter(user=self.request.user).first()
        form.instance.creador_de_reserva = user_profile
        form.instance.cancha = Cancha.objects.get(id=self.kwargs['pk'])
        form.instance.pendiente = True
        form.instance.codigo_operacion = self.request.POST.get('codigo_operacion')
        
        return super(ReservaCreate, self).form_valid(form)



class ReservaDetail(DetailView):
    model = Reserva
    form_class = ReservaForm
    template_name = 'reserva/reserva_detail.html'


class ReservaUpdate(UpdateView):
    model = Reserva
    form_class = ReservaFormAsistencia
    template_name = 'reserva/reserva_update.html'

    def get_success_url(self): 
        #change redirect
        return reverse('reservas_backoffice')


def aceptar_reserva(request, pk):
    reserva = Reserva.objects.get(id=pk)
    try:
        reserva.confirmada = True
        reserva.cancelada = False
        reserva.pendiente = False
        reserva.save()
    except:
        pass
    site = Site.objects.get_current()
    mail_txt = render_to_string('mail_aceptar_reserva.html', {'reserva': reserva})
    print("ENVIO MAIL")
    msg = EmailMultiAlternatives(
        u' Actualizacion de reserva, el estado es: Aceptada - Mis Canchas /ref. #%s' % (reserva.id),
        mail_txt, 'no-reply@miscanchas.com', [reserva.creador_de_reserva.user.email],)
        #cc=['no-reply@miscanchas.com'])
    msg.send()
    return HttpResponseRedirect(reverse('reservas_backoffice'))


@csrf_exempt
def cancelar_reserva(request, pk):
    reserva = Reserva.objects.get(id=pk)
    try:
        reserva.cancelada = True
        reserva.confirmada = False
        reserva.pendiente = False
        reserva.save()
    except:
        pass
    mp = mercadopago.MP(settings.MP_CLIENT_ID, settings.MP_CLIENT_SECRET)
    if settings.MP_SANDBOX_MODE:
        mp.sandbox_mode(True)
    if reserva.estado == 'acreditada':
        result = mp.refund_payment(reserva.mp_id)

        if result['status'] == 'refunded':

            reserva.estado = 'reintegrada'

            reserva.save()

    mail_txt = render_to_string('mail_aceptar_reserva.html', {'reserva': reserva})

    try:
        msg = EmailMultiAlternatives(
            u' Actualizacion de reserva, el estado es: Cancelada - Mis Canchas /ref. #%s' % (reserva.id),
            mail_txt, 'no-reply@miscanchas.com', [reserva.creador_de_reserva.user.email],)
            #cc=['no-reply@miscanchas.com'])
        msg.send()
    except Exception as err:
        print(str(err))

    return HttpResponseRedirect(reverse('reservas_backoffice'))


def cancelar_reserva_fe(request, pk):
    reserva = Reserva.objects.get(id=pk)

    #try:
    reserva.confirmada = False
    reserva.pendiente = False
    reserva.cancelada_por_cliente = True
    reserva.save()
    #except:
    #    pass
    
    if hasattr(request.user, 'empleado') or hasattr(request.user, 'dueno'):
        return HttpResponseRedirect(reverse('reservas_backoffice'))
    else:
        return HttpResponseRedirect(reverse('reservas_list_fe'))


def reservas_serialized(request):
    reservas_full = []
    reservas_json = []
    if hasattr(request.user, 'empleado'):
        establecimientos = Establecimiento.objects.filter(owner=request.user.empleado.empleador)
    else:
        establecimientos = Establecimiento.objects.filter(owner=request.user.dueno)
    for establecimiento in establecimientos:
        canchas = establecimiento.canchas.all()
        for cancha in canchas:
            try:
                reservas = cancha.reservas.filter(estado='acreditada', cancelada_por_cliente=False)
                reservas_full += reservas
            except:
                pass
    for reserva in reservas_full:
        #this check should be in the form valid not here with this try except
        try:
            dic = model_to_dict(reserva, fields=['id', 'periodo', 'cancha', 'fecha'])
            plain_dic = {}
            periodo = dic['periodo'].split('a')
            horario_inicio = periodo[0].split('Hs')[0] if len(periodo[0].split('Hs')[0]) == 5 else '0' + periodo[0].split('Hs')[0]
            horario_fin = periodo[1].split('Hs')[0].strip() if len(periodo[1].split('Hs')[0].strip()) == 5 else '0'+periodo[1].split('Hs')[0].strip()
            plain_dic['title'] = str(Cancha.objects.get(id=dic['cancha']).nombre)
            plain_dic['start'] = dic['fecha'].strftime('%Y-%m-%d') + ' ' + horario_inicio
            plain_dic['end'] = dic['fecha'].strftime('%Y-%m-%d') + ' ' + horario_fin
            plain_dic['name'] = reserva.creador_de_reserva.nombre
            plain_dic['surname'] = reserva.creador_de_reserva.apellido
            plain_dic['email'] = reserva.creador_de_reserva.user.email
            plain_dic['url'] = "http://miscanchas.com/backoffice/reservas/" + str(dic['id']) + "/detail/"
        except:
            pass
        reservas_json.append(plain_dic)
    app_json = json.dumps(reservas_json)
    #reservas_as_json = serializers.serialize('json', reservas_full)
    return HttpResponse([app_json], content_type='json')

class FacturacionList(ListView):
    model = Facturacion
    template_name = 'facturacion/facturacion_list.html'

    def get_queryset(self):
        facturacion_list = []
        qs = super(FacturacionList, self).get_queryset()
        if hasattr(self.request.user, 'empleado'):
            
            establecimientos = Establecimiento.objects.filter(owner=self.request.user.empleado.empleador)
        else:
            
            establecimientos = Establecimiento.objects.filter(owner=self.request.user.dueno)
        for establecimiento in establecimientos:
            try:
                facturacion_list.append(establecimiento.facturacion)
            except:
                pass
        
        return facturacion_list


class ReservaList(ListView):
    model = Reserva
    template_name = 'reserva/reserva_list.html'

    def get_queryset(self):
        reservas_full = []
        qs = super(ReservaList, self).get_queryset()
        if hasattr(self.request.user, 'empleado'):
            
            establecimientos = Establecimiento.objects.filter(owner=self.request.user.empleado.empleador)
        else:
            
            establecimientos = Establecimiento.objects.filter(owner=self.request.user.dueno)
        for establecimiento in establecimientos:
            canchas = establecimiento.canchas.all()
            for cancha in canchas:
                
                try:
                    reservas = cancha.reservas.filter(
                        Q(confirmada=True) | Q(cancelada=True) | Q(pendiente=True))
                    reservas_full += reservas
                except:
                    pass
        # Ordeno por fecha, chequear si esta correcto
        reservas_full.sort(key=lambda x: x.fecha, reverse=False)
        return reservas_full


class ReservasCanceladasList(ListView):
    model = Reserva
    template_name = 'reserva/reserva_cancelaciones.html'

    def get_queryset(self):
        reservas_full = []
        qs = super(ReservasCanceladasList, self).get_queryset()
        if hasattr(self.request.user, 'empleado'):
            
            establecimientos = Establecimiento.objects.filter(owner=self.request.user.empleado.empleador)
        else:
            
            establecimientos = Establecimiento.objects.filter(owner=self.request.user.dueno)
        for establecimiento in establecimientos:
            canchas = establecimiento.canchas.all()
            for cancha in canchas:
                
                try:
                    reservas = cancha.reservas.filter(cancelada_por_cliente=True)
                    reservas_full += reservas
                except:
                    pass
        return reservas_full


class ReservasCanceladasListFull(ListView):
    model = Reserva
    template_name = 'reserva/reserva_cancelaciones_admin.html'

    def get_queryset(self):
        reservas_full = []
        qs = super(ReservasCanceladasListFull, self).get_queryset()
        establecimientos = Establecimiento.objects.all()
        for establecimiento in establecimientos:
            canchas = establecimiento.canchas.all()
            for cancha in canchas:
                
                try:
                    reservas = cancha.reservas.filter(cancelada_por_cliente=True)
                    reservas_full += reservas
                except:
                    pass
        
        return reservas_full


class CalendarView(ListView):
    model = Reserva
    template_name = 'reserva/reserva_calendar.html'

    def get_queryset(self):
        reservas_full = []
        qs = super(CalendarView, self).get_queryset()
        if hasattr(self.request.user, 'empleado'):
            
            establecimientos = Establecimiento.objects.filter(owner=self.request.user.empleado.empleador)
        else:
            establecimientos = Establecimiento.objects.filter(owner=self.request.user.dueno)
        for establecimiento in establecimientos:
            canchas = establecimiento.canchas.all()
            for cancha in canchas:
                
                try:
                    reservas = cancha.reservas.filter(confirmada=True)
                    reservas_full += reservas
                except:
                    pass
        return reservas_full


class ReservaListFront(ListView):
    model = Reserva
    template_name = 'reserva/reserva_list_public.html'
    ordering = ['fecha']

    def get_queryset(self):
        qs = super(ReservaListFront, self).get_queryset()
        #cambiar la lista de reservas
        reservas = Reserva.objects.filter(creador_de_reserva=self.request.user.profile).order_by('-fecha')
        
        return reservas

    def get_context_data(self, **kwargs):
        context = super(ReservaListFront, self).get_context_data(**kwargs)
        context['reservas'] = Reserva.objects.filter(creador_de_reserva=self.request.user.profile)
        return context


class FavoritoList(ListView):
    model = Favorito
    template_name = 'cancha/favorito_list.html'


class FavoritoDelete(DeleteView):
    model = Favorito

    def get(self, *a, **kw):
        return self.delete(*a, **kw)

    def get_success_url(self): 
        return reverse('favorito_list')


def add_fav(request, establecimiento_id, pk):
    cancha = Cancha.objects.get(id=pk)
    user = request.user.profile
    try:
        fav = Favorito.objects.get(Q(cancha=cancha) & Q(usuario=user))
    except:
        fav = False
    if fav:
        # Manejar?
        return HttpResponseRedirect(reverse('favorito_list'))
    else:
        new_fav = Favorito()
        new_fav.usuario = user
        new_fav.cancha = cancha
        new_fav.save()
    return HttpResponseRedirect(reverse('favorito_list'))


def new_employee(request):
    """ Vista para crear un nuevo usuario empleado"""

    if request.method == 'POST':
        form = EmailUserCreationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password2']
            user = get_user_model().objects.create_user(
                email=email, password=password
            )
            user.save()

            request.session['employee_user'] = user.id

            return HttpResponseRedirect(reverse('new_employee_profile'))
    else:
        form = EmailUserCreationForm()

    context = {'form': form, }
    return render(request, 'empleado/new_empleado.html', context)


class FacturacionCreate(CreateView):
    model = Facturacion
    form_class = FacturacionForm
    template_name = 'facturacion/facturacion_create.html'

    def get_success_url(self):
        return reverse('establecimiento_detail', kwargs={'pk': self.kwargs['pk']})

    def get_form_kwargs(self):
        kwargs = super(FacturacionCreate, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

class FacturacionUpdate(UpdateView):
    model = Facturacion
    form_class = FacturacionForm
    template_name = 'facturacion/facturacion_update.html'

    def get_success_url(self): 
        #change redirect
        return reverse('establecimiento_detail', kwargs={'pk': self.kwargs['pk']})

    def get_form_kwargs(self):
        kwargs = super(FacturacionUpdate, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs


class EmpleadoEstablecimientoCreate(CreateView):
    model = EmpleadoEstablecimiento
    form_class = EmpleadoEstablecimientoForm
    template_name = 'empleado/empleado_new_profile.html'

    def get_success_url(self):
        return reverse('home_backoffice')

    def form_valid(self, form):
        user = get_user_model().objects.get(id=self.request.session.get('employee_user'))
        form.instance.user = user
        form.instance.empleador = self.request.user.dueno
        return super(EmpleadoEstablecimientoCreate, self).form_valid(form)

    def dispatch(self, *args, **kwargs):
        return super(EmpleadoEstablecimientoCreate, self).dispatch(*args, **kwargs)


class EmpleadoEstablecimientoList(ListView):
    model = EmpleadoEstablecimiento
    template_name = 'empleado/empleado_list.html'

    def get_queryset(self):
        qs = super(EmpleadoEstablecimientoList, self).get_queryset()
        #cambiar la lista de reservas
        empleados = self.request.user.dueno.empleados.all()
        return empleados


class EmpleadoEstablecimientoUpdate(UpdateView):
    model = EmpleadoEstablecimiento
    form_class = EmpleadoEstablecimientoForm
    template_name = 'empleado/empleado_update.html'


class ContactFormView(FormView):

    form_class = ContactForm
    template_name = "info/email_form.html"
    success_url = 'email-sent'

    def form_valid(self, form):
        mensaje = "{nombre} / {email} dijo: ".format(
            nombre=form.cleaned_data.get('nombre'),
            email=form.cleaned_data.get('email'))
        mensaje += "\n\n{0}".format(smart_str(form.cleaned_data.get('mensaje')))
        send_mail(
            subject=smart_str(form.cleaned_data.get('asunto').strip()),
            message=smart_str(mensaje),
            from_email=form.cleaned_data.get('email'),
            recipient_list=[settings.RECIPIENT_EMAIL],
            fail_silentl=False
        )

        return super(ContactFormView, self).form_valid(form)

    def get_success_url(self): 
        return reverse('email-sent')


def busqueda_cancha(request, *args, **kwargs):
    f = CanchaFilter(request.GET, queryset=Cancha.objects.all())
    # f = Cancha.objects.all()
    return render(request, 'cancha/cancha_busqueda_fe.html', {'filter': f})


@csrf_exempt
def mp_notification(request):
    mp = mercadopago.MP(settings.MP_CLIENT_ID, settings.MP_CLIENT_SECRET)
    if settings.MP_SANDBOX_MODE:
        mp.sandbox_mode(True)
    print("MP NOTIFICATION")
    print(request.GET)

    if request.GET.get('topic', '') == 'payment':
        site = Site.objects.get_current()
        print(request.GET["id"])

        payment_info = mp.get_payment_info(request.GET["id"])
        print(payment_info)
        send_mail('MP payment info - %s' % site.name, json.dumps(payment_info, indent=2), 'test@socialbits.net',
                  ['test@socialbits.net'], fail_silently=False)

        print('Payment info {}'.format(payment_info['status']))
        if payment_info['status'] == 200:
            mp_id = payment_info['response']['collection']['external_reference']
            status = payment_info['response']['collection']['status']
            if status == 'approved':
                reserva = get_object_or_404(Reserva, mp_id=mp_id)

                reserva.estado = 'acreditada'
                reserva.fecha_deposito_reserva = datetime.now()
                reserva.deposito_reserva = reserva.costo_total
                reserva.save()

                mail_txt = render_to_string('mail_mp_txt.html', {'reserva': reserva})

                try:
                    msg = EmailMultiAlternatives(
                        u'Confirmacion de Reserva %s - Mis Canchas /ref. #%s' % (site.name, reserva.id),
                        mail_txt, 'no-reply@miscanchas.com', [reserva.creador_de_reserva.user.email],
                        cc=['no-reply@miscanchas.com'])
                    msg.send()
                except Exception as err:
                    print(str(err))

            return HttpResponse('ok')
    return Http404('bad boy')


@never_cache
@csrf_exempt
def ipn_paypal(request, codigo_operacion, con_luz, fecha, periodo_index, cancha_id):
    periodo = TIME_CHOICES[periodo_index][0]
    user_profile = UserProfile.objects.filter(user=request.user).first()
    cancha = Cancha.objects.get(id=cancha_id)
    reserva = Reserva.objects.create(
        codigo_operacion=codigo_operacion,
        con_luz=bool(con_luz.capitalize()),
        periodo=periodo,
        fecha=fecha,
        creador_de_reserva=user_profile,
        cancha=cancha,
        pendiente=False,
        confirmada=True
    )

    print(request.body)
    if reserva.is_paypal_reserva_pago(request_body=request.body):
        try:
            reserva.estado = 'acreditada'
            reserva.fecha_deposito_reserva = datetime.now()
            reserva.save()
        except Exception as err:
            raise Http404('Error finalizing purchase', err)
        
        
        site = Site.objects.get_current()    
        mail_txt = render_to_string('mail_mp_txt.html', {'reserva': reserva})
        try:
            msg = EmailMultiAlternatives(
                u'Recibimos tu reserva %s - Mis Canchas /ref. #%s' % (site.name, reserva.id),
                mail_txt, 'no-reply@miscanchas.com', [reserva.creador_de_reserva.user.email],)
                #cc=['no-reply@miscanchas.com'])
            msg.send()
        except Exception as err:
            print(str(err))

        return render(request, 'gracias_mp.html', {'gracias': True, 'reserva': reserva})
    else:
        return Http404('bad boy')


class CancelacionesUpdate(UpdateView):
    model = Reserva
    form_class = CancelacionForm
    template_name = 'reserva/cancelacion_update.html'

    def get_success_url(self): 
        return reverse('reservas_canceladas')


class CancelacionesUpdateAdmin(UpdateView):
    model = Reserva
    form_class = CancelacionForm
    template_name = 'reserva/cancelacion_update_admin.html'

    def get_success_url(self): 
        return reverse('reservas_canceladas_admin')



########################
# Guardo esto para un posible revert de funcionalidad.
# def disponibilidad_cancha(request, year, month, day, establecimiento_id, cancha_id):
#     plain = []
#     cancha = Cancha.objects.get(id=cancha_id)
#     data = {el: False for el in HOUR_OF_DAY_24}
#     #data = {el[0]: False for el in PERIOD_HOUR}
#     schedule = OrderedDict(sorted(data.items()))
#     bookings = OrderedDict(sorted(data.items()))

#     date = str(day) + '/' + str(month) + '/' + str(year)
#     fecha = datetime.strptime(date, '%d/%m/%Y').date()
#     reservas = Reserva.objects.filter(cancha=cancha, fecha=fecha)

#     dia_de_la_semana_numero = fecha.isoweekday()
#     if dia_de_la_semana_numero == 1:

#         hora_inicio, minuto_inicio = cancha.desde_lunes.hour, cancha.desde_lunes.minute
#         hora_fin, minuto_fin = cancha.hasta_lunes.hour, cancha.hasta_lunes.minute
#         inicio = (hora_inicio, minuto_inicio)
#         fin = (hora_fin, minuto_fin)

#         for key, value in schedule.items():
#             if inicio <= key <= fin:
#                 schedule[key] = True

#         #CHEQUEO Doble turno
#         if cancha.lunes_doble_turno:
#             hora_inicio2, minuto_inicio2 = cancha.desde_lunes_tarde.hour, cancha.desde_lunes_tarde.minute
#             hora_fin2, minuto_fin2 = cancha.hasta_lunes_tarde.hour, cancha.hasta_lunes_tarde.minute
#             inicio2 = (hora_inicio2, minuto_inicio2)
#             fin2 = (hora_fin2, minuto_fin2)
#             for key, value in schedule.items():
#                 if inicio2 <= key <= fin2:
#                     schedule[key] = True


#     elif dia_de_la_semana_numero == 2:

#         hora_inicio, minuto_inicio = cancha.desde_martes.hour, cancha.desde_martes.minute
#         hora_fin, minuto_fin = cancha.hasta_martes.hour, cancha.hasta_martes.minute
#         inicio = (hora_inicio, minuto_inicio)
#         fin = (hora_fin, minuto_fin)

#         for key, value in schedule.items():
#             if inicio <= key <= fin:
#                 schedule[key] = True

#         #CHEQUEO Doble turno
#         if cancha.martes_doble_turno:
#             hora_inicio2, minuto_inicio2 = cancha.desde_martes_tarde.hour, cancha.desde_martes_tarde.minute
#             hora_fin2, minuto_fin2 = cancha.hasta_martes_tarde.hour, cancha.hasta_martes_tarde.minute
#             incio2 = (hora_inicio2, minuto_inicio2)
#             fin2 = (hora_fin2, minuto_fin2)
#             for key, value in schedule.items():
#                 if inicio2 <= key <= fin2:
#                     schedule[key] = True

#     elif dia_de_la_semana_numero == 3:
#         hora_inicio, minuto_inicio = cancha.desde_miercoles.hour, cancha.desde_miercoles.minute
#         hora_fin, minuto_fin = cancha.hasta_miercoles.hour, cancha.hasta_miercoles.minute
#         inicio = (hora_inicio, minuto_inicio)
#         fin = (hora_fin, minuto_fin)

#         for key, value in schedule.items():
#             if inicio <= key <= fin:
#                 schedule[key] = True

#         #CHEQUEO Doble turno
#         if cancha.miercoles_doble_turno:
#             hora_inicio2, minuto_inicio2 = cancha.desde_miercoles_tarde.hour, cancha.desde_miercoles_tarde.minute
#             hora_fin2, minuto_fin2 = cancha.hasta_miercoles_tarde.hour, cancha.hasta_miercoles_tarde.minute
#             incio2 = (hora_inicio2, minuto_inicio2)
#             fin2 = (hora_fin2, minuto_fin2)
#             for key, value in schedule.items():
#                 if inicio2 <= key <= fin2:
#                     schedule[key] = True

#     elif dia_de_la_semana_numero == 4:
#         hora_inicio, minuto_inicio = cancha.desde_jueves.hour, cancha.desde_jueves.minute
#         hora_fin, minuto_fin = cancha.hasta_jueves.hour, cancha.hasta_jueves.minute
#         inicio = (hora_inicio, minuto_inicio)
#         fin = (hora_fin, minuto_fin)

#         for key, value in schedule.items():
#             if inicio <= key <= fin:
#                 schedule[key] = True

#         #CHEQUEO Doble turno
#         if cancha.jueves_doble_turno:
#             hora_inicio2, minuto_inicio2 = cancha.desde_jueves_tarde.hour, cancha.desde_jueves_tarde.minute
#             hora_fin2, minuto_fin2 = cancha.hasta_jueves_tarde.hour, cancha.hasta_jueves_tarde.minute
#             incio2 = (hora_inicio2, minuto_inicio2)
#             fin2 = (hora_fin2, minuto_fin2)
#             for key, value in schedule.items():
#                 if inicio2 <= key <= fin2:
#                     schedule[key] = True

#     elif dia_de_la_semana_numero == 5:
#         hora_inicio, minuto_inicio = cancha.desde_viernes.hour, cancha.desde_viernes.minute
#         hora_fin, minuto_fin = cancha.hasta_viernes.hour, cancha.hasta_viernes.minute
#         inicio = (hora_inicio, minuto_inicio)
#         fin = (hora_fin, minuto_fin)

#         for key, value in schedule.items():
#             if inicio <= key <= fin:
#                 schedule[key] = True

#         #CHEQUEO Doble turno
#         if cancha.viernes_doble_turno:
#             hora_inicio2, minuto_inicio2 = cancha.desde_viernes_tarde.hour, cancha.desde_viernes_tarde.minute
#             hora_fin2, minuto_fin2 = cancha.hasta_viernes_tarde.hour, cancha.hasta_viernes_tarde.minute
#             incio2 = (hora_inicio2, minuto_inicio2)
#             fin2 = (hora_fin2, minuto_fin2)
#             for key, value in schedule.items():
#                 if inicio2 <= key <= fin2:
#                     schedule[key] = True
#     elif dia_de_la_semana_numero == 6:
#         hora_inicio, minuto_inicio = cancha.desde_sabado.hour, cancha.desde_sabado.minute
#         hora_fin, minuto_fin = cancha.hasta_sabado.hour, cancha.hasta_sabado.minute
#         inicio = (hora_inicio, minuto_inicio)
#         fin = (hora_fin, minuto_fin)

#         for key, value in schedule.items():
#             if inicio <= key <= fin:
#                 schedule[key] = True

#         #CHEQUEO Doble turno
#         if cancha.sabado_doble_turno:
#             hora_inicio2, minuto_inicio2 = cancha.desde_sabado_tarde.hour, cancha.desde_sabado_tarde.minute
#             hora_fin2, minuto_fin2 = cancha.hasta_sabado_tarde.hour, cancha.hasta_sabado_tarde.minute
#             incio2 = (hora_inicio2, minuto_inicio2)
#             fin2 = (hora_fin2, minuto_fin2)
#             for key, value in schedule.items():
#                 if inicio2 <= key <= fin2:
#                     schedule[key] = True
#     elif dia_de_la_semana_numero == 7:
#         hora_inicio, minuto_inicio = cancha.desde_domingo.hour, cancha.desde_domingo.minute
#         hora_fin, minuto_fin = cancha.hasta_domingo.hour, cancha.hasta_domingo.minute
#         inicio = (hora_inicio, minuto_inicio)
#         fin = (hora_fin, minuto_fin)

#         for key, value in schedule.items():
#             if inicio <= key <= fin:
#                 schedule[key] = True

#         #CHEQUEO Doble turno
#         if cancha.domingo_doble_turno:
#             hora_inicio2, minuto_inicio2 = cancha.desde_domingo_tarde.hour, cancha.desde_domingo_tarde.minute
#             hora_fin2, minuto_fin2 = cancha.hasta_domingo_tarde.hour, cancha.hasta_domingo_tarde.minute
#             incio2 = (hora_inicio2, minuto_inicio2)
#             fin2 = (hora_fin2, minuto_fin2)
#             for key, value in schedule.items():
#                 if inicio2 <= key <= fin2:
#                     schedule[key] = True

#     for reserva in reservas:
#         hora_inicio_reserva, minuto_inicio_reserva = reserva.horario_inicio.hour, reserva.horario_inicio.minute
#         hora_fin_reserva, minuto_fin_reserva = reserva.horario_fin.hour, reserva.horario_fin.minute
#         inicio_reserva = (hora_inicio_reserva, minuto_inicio_reserva)
#         fin_reserva = (hora_fin_reserva, minuto_fin_reserva)
#         for key, value in schedule.items():
#             if inicio_reserva <= key <= fin_reserva:
#                 bookings[key] = True

#     result = OrderedDict()
#     for key, value in schedule.items():
#         result = OrderedDict()

#         hora = str(key[0])
#         minuto = str(key[1])
#         if len(hora) == 1:
#             hora = "0" + str(key[0])
#         if len(minuto) == 1:
#             minuto = "0" + str(key[1])

#         result['time'] = hora + ':' + minuto

#         if bookings[key]:
#             result['status'] = 'reservado'
#         elif schedule[key]:
#             result['status'] = 'disponible'
#         else:
#             result['status'] = 'disabled'
#         plain.append(result)
#     app_json = json.dumps(plain)
#     return HttpResponse(app_json, content_type='json')
