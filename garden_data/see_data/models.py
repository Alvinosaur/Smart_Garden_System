from django.db import models
from django import utils

class Owner(models.Model):
	name = models.CharField(max_length=50,default="Alvin")
	
	def __str__(self):
		return self.name

class Species(models.Model):
	species = models.CharField(max_length=50,default="Strawberry")
	optimal_light = models.IntegerField(default=65)
	optimal_moist = models.IntegerField(default=60)
	optimal_heat = models.IntegerField(default=60)

	def __str__(self):
		return self.species

class Plant(models.Model):
	owner = models.ForeignKey(Owner,on_delete=models.CASCADE,null=True)
	species = models.ForeignKey(Species,on_delete=models.CASCADE,null=True)
	image = models.CharField(max_length=100,default='http://www.ciaoimports.com/assets/images/Strawberry.jpg')
	locX = models.IntegerField(default=0)
	locY = models.IntegerField(default=0)
	start_date = models.DateField(default=utils.timezone.now) #from datetime import date
	current_size = models.IntegerField(default=3)
	current_moist = models.IntegerField(default=50)
	current_light = models.IntegerField(default=60)
	current_heat = models.IntegerField(default=70)
	is_favorite = models.BooleanField(default=False)
	all_moist = [current_moist]
	all_heat = [current_heat]
	all_light = [current_light]

	def __str__(self):
		return "%s plant at (%d,%d)"%(self.species,self.locX,self.locY)



