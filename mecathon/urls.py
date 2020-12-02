"""mecathon URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import include, path
from django.contrib import admin
from django.urls import path
from core import views
urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Registro do usuário e criação do mesmo

    path('login/',views.loginUser),
    path('register/',views.register),
    path('get_user_info',views.get_user_info),
    path('get_selections_mentor',views.get_selections_mentor),
    path("check_user_type",views.check_user_type),

    # Time
    path('create_team/',views.create_team),
    path('integrate_team/',views.integrate_team),
    path('getout_team/',views.getout_team),
    path('get_teams',views.get_teams), # Obter a lista dos times 
    path('integrate_team',views.integrate_team), #integração de times
    path('sendprojectlink',views.sendprojectlink),

    # mentores
    path('show_disposable_mentors/',views.show_disposable_mentors),
    path('select_mentor/',views.select_mentor),
    path('insert_data_meeting/',views.insert_data_meeting),

    
    #Jurado
    path('set_points',views.set_points), # dar nota
    path('get_listOf_project',views.get_listOf_project),
    

    # Criação do desafio
    path('challenge/',views.create_challenge), #Não implementado!


]
