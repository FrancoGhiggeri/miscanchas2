# -*- coding: utf-8 -*-

#from django.core.urlresolvers import reverse
from django.urls import reverse
from django.http import HttpResponseRedirect


def owner_required(view_func):
    def _wrapped_view_func(request, *args, **kwargs):
        if not hasattr(request.user, 'dueno') or hasattr(request.user, 'empleado'):
            return HttpResponseRedirect(reverse('home'))
        return view_func(request, *args, **kwargs)
    return _wrapped_view_func
