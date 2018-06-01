from django.urls import path
from see_data import views

app_name = "see_data"

urlpatterns = [
    path('',views.index,name='index'),

    #store integer into plant_id and pass into detail() function
    path('see_data/<int:plant_id>/', views.detail, name='detail'),

    path('see_data/<int:plant_id>/favorite/',views.favorite,name='favorite'),
]