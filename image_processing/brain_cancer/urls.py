from django.urls import path
from . import views

urlpatterns = [

    # the path to main show
    path('', views.process_image, name='brain_cancer_home'),
]
