from django.shortcuts import render, redirect

import callboard.views.index
from callboard.models import Advert
from django.views.generic import View
from django.http.response import HttpResponse


class Index(View):   # пока закомментировал (убрал контекст)

    def get(self, request):
        models = Advert.objects.all()
        context = {
            'models': models,
        }
        return HttpResponse(render(request, 'callboard/index.html', ))

