from django.shortcuts import render

from .models import Area


def index(request):
    area_list = Area.objects.order_by('id')
    context = {'area_list': area_list}
    return render(request, 'measurements/index.html', context)
