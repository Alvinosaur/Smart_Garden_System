from django.shortcuts import render, get_object_or_404
from .models import Plant

#request is the HTTP website url
def index(request):
	all_plants = Plant.objects.all()

	#context is standard name for dict that holds info used by template
	context = {"all_plants":all_plants
			}
	return render(request,'see_data/index.html',context)


def detail(request,plant_id):
	plant = get_object_or_404(Plant,pk=plant_id)
	return render(request,'see_data/detail.html',{'plant':plant})

def favorite(request,plant_id):
	selected_plant = get_object_or_404(Plant,pk=plant_id)
	try:
		selected_plant = get_object_or_404(Plant,pk=plant_id)
		#selected_plant= plant.owner.plant_set.get(pk=request.POST['plant'])
	except (KeyError, Plant.DoesNotExist):
		return render(request,'see_data/detail.html',{
			'plant':selected_plant,
			'error_message':"You didn't select a valid plant",
		})
	else:
		if selected_plant.is_favorite:
			selected_plant.is_favorite = False
		else:
			selected_plant.is_favorite = True
		selected_plant.save()
	return render(request,'see_data/detail.html',{'plant':selected_plant})
