from django.shortcuts import render
from django.http import HttpResponse
from .models import Plants

#request is the HTTP website url
def index(request):
	all_plants = Plants.objects.all()
	html = ''
	for plant in all_plants:
		#every plant has a bulit-in unique id like a hash, so use this
		url = '/see_data/' + str(plant.id) + '/'

		#link urls to different html phrases
		html += '<a href="' + url + '">' + plant.species + ": " + plant.instance + '</a><br>'
	header = "<h1>Plants:</h1>"
	table = html
	return HttpResponse(header + table)


def detail(request,plant_id):
	return HttpResponse("<h2>Details for plant id: " + str(plant_id) + "</h2>")


