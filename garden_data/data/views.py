from django.shortcuts import render, get_object_or_404
from .models import Plant

#request is the HTTP website url
def home(request):
	all_owners = Owner.objects.all()

	#map all owners to the parameter, all_owners, and pass into home.html 
	return render(request,'data/home.html',{"all_owners":all_owners})

def index(request,owner_id):
	owner = get_object_or_404(Owner,pk=owner_id)
	return render(request,'data/index.html',{"owner":owner})

def favorite(request,owner_id):
	owner = get_object_or_404(Owner,pk=owner_id)
	try:
		selected_species= owner.species_set.get(pk=request.POST['species'])
	except (KeyError, Species.DoesNotExist):
		return render(request,'data/index.html',{
			'species':selected_species,
			'error_message':"You didn't select a valid species",
		})
	else:
		if selected_species.is_favorite:
			selected_species.is_favorite = False
		else:
			selected_species.is_favorite = True
		selected_species.save()
	return render(request,'data/index.html',{'species':selected_species})

def detail(request,species_id):
	species = get_object_or_404(Species,pk=species_id)
	return render(request,'data/detail.html',{"species":species})

def sub_detail(request,plant_id):
	plant = get_object_or_404(Plant,pk=plant_id)
	return render(request,'data/sub_detail.html',{'plant':plant})



