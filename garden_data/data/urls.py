from django.urls import path
from data import views

app_name = "data"


urlpatterns = [
    path('',views.home,name='home'),

    path('%s/%s_<int:owner_id>/'%(app_name,owner), views.index, name='index'),
    path('%s/%s_%d/%s_<int:species_id>'%(app_name,owner,owner_id,species), views.detail, name='detail'),
    path('%s/%s_%d/%s_<int:species_id>/favorite'%(app_name,owner,owner_id), views.favorite, name='favorite'),
    path('%s/%s_%d/%s_%d/%s_<int:plant_id>'%(app_name,owner,owner_id,species,species_id,plant), views.sub_detail, name='sub_detail'),
]