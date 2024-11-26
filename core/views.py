from django.shortcuts import render, HttpResponse
from autenticacion.models import Usuario
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# import pytz
@login_required(login_url='login1')
def menu(request):
    user = request.user.username
    usuario = Usuario.objects.get(username=user)
    departamento = usuario.departamento

    if departamento == "Inventario":
        messages.success(request, f'Inicio Exitoso!, Bienvenido!, {request.user.username}')
        return render(request, 'menu_sistema.html')












