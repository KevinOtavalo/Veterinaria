from django import forms
from .models import Mascota, PerfilUsuario, Vacuna, ConsultaVeterinaria
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.contrib.auth.models import User


class MascotaForm(forms.ModelForm):
    dueño = forms.ModelChoiceField(
        queryset=User.objects.all(), required=False)  # Para staff

    class Meta:
        model = Mascota
        fields = ['nombre', 'especie', 'raza', 'fecha_nacimiento', 'dueño']
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        is_staff = kwargs.pop('is_staff', False)
        super().__init__(*args, **kwargs)
        if not is_staff:
            self.fields['dueño'].widget = forms.HiddenInput()
            self.fields['dueño'].required = False
        else:
            self.fields['dueño'].required = True

    def clean_fecha_nacimiento(self):
        fecha = self.cleaned_data['fecha_nacimiento']
        if fecha > timezone.now().date():
            raise ValidationError(
                "La fecha de nacimiento no puede ser en el futuro.")
        return fecha


class PerfilUsuarioForm(forms.ModelForm):
    class Meta:
        model = PerfilUsuario
        fields = ['nombre_completo', 'direccion', 'edad', 'rut']


class VacunaForm(forms.ModelForm):
    class Meta:
        model = Vacuna
        fields = ['nombre', 'fecha_aplicacion', 'proxima_dosis']
        widgets = {
            'fecha_aplicacion': forms.DateInput(attrs={'type': 'date'}),
            'proxima_dosis': forms.DateInput(attrs={'type': 'date'}),
        }


class ConsultaVeterinariaForm(forms.ModelForm):
    class Meta:
        model = ConsultaVeterinaria
        fields = ['motivo', 'diagnostico', 'tratamiento']
        widgets = {
            'motivo': forms.Textarea(attrs={'rows': 2}),
            'diagnostico': forms.Textarea(attrs={'rows': 2}),
            'tratamiento': forms.Textarea(attrs={'rows': 2}),
        }
