from django.shortcuts import render
from django.http import HttpResponse, Http404
from .models import Plants

#request is the HTTP website url
def index(request):
	all_plants = Plants.objects.all()

	#context is standard name for dict that holds info used by template
	context = {"all_plants":all_plants
			}
	return render(request,'see_data/index.html',context)


def detail(request,plant_id):
	try:
		plant = Plants.objects.get(pk=plant_id)
	except Plants.DoesNotExist:
		raise Http404("Plant does not exist")
	return render(request,'see_data/detail.html',{"plant":plant})


