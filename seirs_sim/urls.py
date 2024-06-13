# meningitis_sim/seirs_sim/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('normal_simulation/', views.normal_simulation, name='normal_simulation'),
    path('normal_simulation_result/', views.normal_simulation_result, name='normal_simulation_result'),
    path('vaccine_simulation/', views.vaccine_simulation, name='vaccine_simulation'),  # view for vaccine simulation
    path('vaccine_simulation_result/<str:probs>/', views.vaccine_simulation_result, name='vaccine_simulation_result'),  # view for vaccine simulation result
]

