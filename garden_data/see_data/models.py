from django.db import models

# Create your models here.
class Plants(models.Model):
	species = models.CharField(max_length=250,default="Strawberry")
	instance = models.CharField(max_length=253,default="plant1")
	image = models.CharField(max_length=100,default='http://www.ciaoimports.com/assets/images/Strawberry.jpg')
	leaves = models.IntegerField(default=4)

	def __str__(self):
		return self.instance + ' - ' + self.species

class Owners(models.Model):
	plant = models.ForeignKey(Plants,on_delete=models.CASCADE)
	


