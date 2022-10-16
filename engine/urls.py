from django.urls import path
from . import views 


urlpatterns = [
    path('',views.query, name="query"),
    path('results', views.results, name="results"),
    path('next', views.next, name="next"),
    path('prev', views.prev, name="prev"),
    path('about', views.about, name="about"),
]
