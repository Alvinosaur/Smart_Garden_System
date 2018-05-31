from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Plants

#request is the HTTP website url
def index(request):
	all_plants = Plants.objects.all()

	#get_template assuems you've created a template folder in current app directory
	template = loader.get_template('see_data/index.html')

	#context is standard name for dict that holds info used by template
	context = {
		"all_plants":all_plants,
	}
	return HttpResponse(template.render(context,request))


def detail(request,plant_id):
	return HttpResponse("<h2>Details for plant id: " + str(plant_id) + "</h2>")


