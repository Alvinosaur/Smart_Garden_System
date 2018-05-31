from django.urls import path
from see_data import views


urlpatterns = [
    path('',views.index,name='index'),

    #store integer into plant_id and pass into detail() function
    path('see_data/<int:plant_id>/', views.detail, name='detail'),
]