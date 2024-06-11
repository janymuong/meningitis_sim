# meningitis_sim/seirs_sim/urls.py


# from django.urls import path
# from . import views

# urlpatterns = [
#     path('simulation/', views.simulation_form, name='simulation_form'),
#     path('simulation/<int:params_id>/', views.run_simulation, name='run_simulation'),
# ]

# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.simulation_form, name='simulation_form'),
#     path('run/<int:params_id>/', views.run_simulation, name='run_simulation'),
# ]


from django.urls import path
from . import views

urlpatterns = [
    path('simulation/', views.normal_simulation, name='normal_simulation'),
    path('result/', views.normal_simulation_result, name='normal_simulation_result'),
]
