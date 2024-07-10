# meningitis_sim/seirs_sim/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # normal simulation route/views, for model visualizations:
    path('normal_simulation/', views.normal_simulation, name='normal_simulation'),
    path('normal_simulation_result/',
         views.normal_simulation_result, name='normal_simulation_result'),
    # view for vaccine simulation, vaccine simulation visualizations:
    path('vaccine_simulation/', views.vaccine_simulation, name='vaccine_simulation'),
    path('vaccine_simulation_result/<str:probs>/',
         views.vaccine_simulation_result, name='vaccine_simulation_result'),
    # these views are the vaccination strategies based on an age range
    path('age_based_vaccine_simulation/',
         views.age_based_vaccine_simulation, name='age_based_vaccine_simulation'),
    path('age_based_vaccine_simulation_result/<str:probs>/',
         views.age_based_vaccine_simulation_result, name='age_based_vaccine_simulation_result'),
    path('treatment_simulation/', views.treatment_simulation, name='treatment_simulation'),
    path('treatment_simulation_result/<str:probs>/',
         views.treatment_simulation_result, name='treatment_simulation_result'),
]
