from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_decode
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from .forms import UsuarioForm, CambiocontraseñaForm
from .models import Usuario
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib import messages
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.shortcuts import render, redirect
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.views import PasswordResetView


def login(request):

    return render(request,'menu.html')

def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, 'Cerro la Seción con Exito!')
    # Redirigir a la página de inicio o a donde desees después del cierre de sesión
    return redirect('login1')
def password_reset_exito(request):
    return render(request,'password_reset_exito.html')
# @login_required(login_url='login1')
def crear_usuario(request):
    if request.method == "POST":
        usuarioForm =  UsuarioForm(request.POST or None)
        if usuarioForm.is_valid():
            usuarioForm.save()
            messages.success(request,'Usuario Creado con Exito!')
            return redirect ('login1')
    else:
        usuarioForm = UsuarioForm()
    return render(request, "crear_usuario.html", {'form':usuarioForm})

def cambiar_contraseña(request):
    if request.method == "POST":
        cambiocontraseñaForm =  CambiocontraseñaForm(request.POST or None)
        if cambiocontraseñaForm.is_valid():
            cambiocontraseñaForm.save()
            messages.success(request, '¡Cambio de Contraseña Exito, Vuelva Iniciar Seción!')
            return redirect ('login1')
    else:
        cambiocontraseñaForm = CambiocontraseñaForm()
    return render(request, "cambio_contraseña.html", {'form':cambiocontraseñaForm})

def eliminar_usuario(request, id):
    if request.method == "POST":
        usuario = get_object_or_404(Usuario, pk=id)
        usuarioForm =  UsuarioForm(request.POST or None, instance=usuario)
        if usuarioForm.is_valid():
            usuarioForm.save()
            return redirect ("consulta_usuario")
    else:
        usuario = get_object_or_404(Usuario, pk=id)
        usuarioForm = UsuarioForm(instance=usuario)
    return render(request, "eliminar_usuario.html", {'form':usuarioForm})


def modificar_usuario(request, id):
    if request.method == "POST":
        usuario = get_object_or_404(Usuario, pk=id)
        usuarioForm = UsuarioForm(request.POST or None, instance=usuario)
        if usuarioForm.is_valid():
            usuarioForm.save()
            return redirect ("consulta_usuario")
    else:
        usuario = get_object_or_404(Usuario, pk=id)
        usuarioForm = UsuarioForm(instance=usuario)
    return render(request, "modificar_usuario.html", {'form':usuarioForm})

@login_required(login_url='login1')
def consulta_usuario(request):
    lista_usuarios = Usuario.objects.filter(estado=1)
    return render(request, "consulta_usuario.html", {'lista_usuarios':lista_usuarios})



def password_reset_request(request):
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data['email']
            associated_users = Usuario.objects.filter(email=data)
            print(associated_users)
            if associated_users.exists():
                for user in associated_users:
                    print(user)
                    subject = "Cambio de contraseña solicitado"
                    email_template_name = "password_reset_email.html"
                    c = {
                        "email": user.email,
                        'domain': '192.168.0.128:8000',
                        'site_name': 'YourSite',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'noreply@epmapas.gob.ec', [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    messages.success(request, 'El enlace para restablecer la contraseña ha sido enviado a tu correo electrónico.')
                    return redirect("/")
            else:
                messages.error(request, 'No existe una cuenta asociada a ese correo electrónico.')
                return render(request=request, template_name="password_reset.html", context={"form": form})

    form = PasswordResetForm()
    return render(request=request, template_name="password_reset.html", context={"form": form})


def my_password_reset_confirm(request, uidb64, token):
        UserModel = get_user_model()
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = UserModel._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            if request.method == 'POST':
                form = SetPasswordForm(user, request.POST)
                if form.is_valid():
                    form.save()
                    # Redirige a una página de confirmación o muestra un mensaje de éxito
                    return redirect('password_reset_exito')
            else:
                form = SetPasswordForm(user)
            return render(request, 'password_reset_confirm.html', {'form': form})
        else:
            # Redirige a una página de error o muestra un mensaje de error
            return render(request, 'invalid_token.html')
