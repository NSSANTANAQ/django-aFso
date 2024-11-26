from django import forms
from .models import Usuario
from django.core.exceptions import ValidationError

class UsuarioForm(forms.ModelForm):

    OPCIONES_COLOR = [
        ('Inventario', 'Inventario'),

    ]

    departamento= forms.ChoiceField(choices=OPCIONES_COLOR,label='Modulo', widget=forms.Select(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmar', widget=forms.PasswordInput)

    class Meta:
        model = Usuario
        fields = ['username', 'email', 'departamento']

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class CambiocontraseñaForm(forms.ModelForm):

    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmar', widget=forms.PasswordInput)

    class Meta:
        model = Usuario
        fields = []


