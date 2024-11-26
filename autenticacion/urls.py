"""Sistema3H URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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

from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('',  auth_views.LoginView.as_view(template_name="login.html"), name="login1"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout_view, name='logout'),
    path('password_reset_exito/', views.password_reset_exito, name="password_reset_exito"),
    path('crear_usuario/', views.crear_usuario, name="crear_usuario"),
    path('cambiar_contraseña/', views.cambiar_contraseña, name="cambiar_contraseña"),
    path('consulta_usuario/', views.consulta_usuario, name="consulta_usuario"),
    path('modificar_usuario/<int:id>', views.modificar_usuario, name="modificar_usuario"),
    path('eliminar_usuario/<int:id>', views.eliminar_usuario, name="eliminar_usuario"),
    path('reset_password/',views.password_reset_request, name="reset_password"),
    path('password_reset_confirm/<uidb64>/<token>/',views.my_password_reset_confirm, name='password_reset_confirm'),


]
