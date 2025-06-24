from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from .models import Mascota, PerfilUsuario, ConsultaVeterinaria, Vacuna
from .forms import MascotaForm, PerfilUsuarioForm, VacunaForm, ConsultaVeterinariaForm


class LoginIndexView(LoginView):
    template_name = 'veterinaria/login_index.html'

    def get_success_url(self):
        if self.request.user.is_staff:
            return reverse_lazy('vista_mascotas_todas')  # Para staff
        else:
            return reverse_lazy('vista_mascotas')  # Para usuarios normales


@login_required
def vista_mascotas(request):
    if request.user.is_staff:
        mascotas = Mascota.objects.all()
    else:
        mascotas = Mascota.objects.filter(dueño=request.user)
    return render(request, 'veterinaria/vista_mascotas.html', {'mascotas': mascotas})


@staff_member_required
def vista_mascotas_todas(request):
    mascotas = Mascota.objects.all()
    return render(request, 'veterinaria/vista_mascotas_todas.html', {'mascotas': mascotas})


@login_required
def dashboard_redirect(request):
    if request.user.is_staff:
        return redirect('vista_mascotas_todas')
    else:
        return redirect('vista_mascotas')


def vista_publica(request):
    mascotas = Mascota.objects.all()
    return render(request, 'veterinaria/publico_mascotas.html', {'mascotas': mascotas})


@login_required
def registrar_mascota(request):
    if request.method == 'POST':
        form = MascotaForm(request.POST, is_staff=request.user.is_staff)
        if form.is_valid():
            fecha = form.cleaned_data.get('fecha_nacimiento')
            if fecha > timezone.now().date():
                messages.error(
                    request, 'La fecha de nacimiento no puede ser mayor a la fecha actual.')
                return render(request, 'veterinaria/registrar_mascota.html', {'form': form})

            mascota = form.save(commit=False)

            if request.user.is_staff:
                dueño = form.cleaned_data.get('dueño')
                if dueño:
                    mascota.dueño = dueño
                else:
                    mascota.dueño = request.user  # fallback
            else:
                mascota.dueño = request.user

            mascota.save()
            messages.success(request, 'Mascota registrada con éxito.')
            return redirect('vista_mascotas')
    else:
        form = MascotaForm(is_staff=request.user.is_staff)

    return render(request, 'veterinaria/registrar_mascota.html', {'form': form})


@login_required
def detalle_mascota(request, mascota_id):
    if request.user.is_staff:
        mascota = get_object_or_404(Mascota, id=mascota_id)
    else:
        mascota = get_object_or_404(Mascota, id=mascota_id, dueño=request.user)

    consultas = mascota.consultas.all()
    vacunas = mascota.vacunas.all()
    return render(request, 'veterinaria/detalle_mascota.html', {
        'mascota': mascota,
        'consultas': consultas,
        'vacunas': vacunas
    })


@login_required
def editar_mascota(request, mascota_id):
    if request.user.is_staff:
        mascota = get_object_or_404(Mascota, id=mascota_id)
    else:
        mascota = get_object_or_404(Mascota, id=mascota_id, dueño=request.user)

    if request.method == 'POST':
        form = MascotaForm(request.POST, instance=mascota,
                           is_staff=request.user.is_staff)
        if form.is_valid():
            mascota = form.save(commit=False)
            # Mantener dueño original para no perderlo
            mascota.dueño = mascota.dueño or Mascota.objects.get(
                id=mascota_id).dueño
            mascota.save()
            messages.success(request, 'Mascota actualizada correctamente.')
            return redirect('vista_mascotas')
    else:
        form = MascotaForm(instance=mascota, is_staff=request.user.is_staff)

    return render(request, 'veterinaria/editar_mascota.html', {'form': form, 'mascota': mascota})


@login_required
def eliminar_mascota(request, mascota_id):
    if request.user.is_staff:
        mascota = get_object_or_404(Mascota, id=mascota_id)
    else:
        mascota = get_object_or_404(Mascota, id=mascota_id, dueño=request.user)

    if request.method == 'POST':
        mascota.delete()
        messages.success(request, 'Mascota eliminada correctamente.')
        return redirect('vista_mascotas')
    return render(request, 'veterinaria/eliminar_mascota.html', {'mascota': mascota})


@login_required
def editar_perfil(request):
    perfil, created = PerfilUsuario.objects.get_or_create(user=request.user)
    form = PerfilUsuarioForm(request.POST or None, instance=perfil)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('vista_mascotas')
    return render(request, 'veterinaria/editar_perfil.html', {'form': form})


@staff_member_required
def registrar_vacuna(request, mascota_id):
    mascota = get_object_or_404(Mascota, id=mascota_id)
    if request.method == 'POST':
        form = VacunaForm(request.POST)
        if form.is_valid():
            vacuna = form.save(commit=False)
            vacuna.mascota = mascota
            vacuna.save()
            return redirect('detalle_mascota', mascota_id=mascota.id)
    else:
        form = VacunaForm()
    return render(request, 'veterinaria/registrar_vacuna.html', {'form': form, 'mascota': mascota})


@staff_member_required
def editar_vacuna(request, vacuna_id):
    vacuna = get_object_or_404(Vacuna, id=vacuna_id)
    if request.method == 'POST':
        form = VacunaForm(request.POST, instance=vacuna)
        if form.is_valid():
            form.save()
            return redirect('detalle_mascota', mascota_id=vacuna.mascota.id)
    else:
        form = VacunaForm(instance=vacuna)
    return render(request, 'veterinaria/editar_vacuna.html', {'form': form, 'vacuna': vacuna})


@staff_member_required
def eliminar_vacuna(request, vacuna_id):
    vacuna = get_object_or_404(Vacuna, id=vacuna_id)
    if request.method == 'POST':
        mascota_id = vacuna.mascota.id
        vacuna.delete()
        return redirect('detalle_mascota', mascota_id=mascota_id)
    return render(request, 'veterinaria/eliminar_vacuna.html', {'vacuna': vacuna})


@staff_member_required
def registrar_consulta(request, mascota_id):
    mascota = get_object_or_404(Mascota, id=mascota_id)
    if request.method == 'POST':
        form = ConsultaVeterinariaForm(request.POST)
        if form.is_valid():
            consulta = form.save(commit=False)
            consulta.mascota = mascota
            consulta.save()
            return redirect('detalle_mascota', mascota_id=mascota.id)
    else:
        form = ConsultaVeterinariaForm()
    return render(request, 'veterinaria/registrar_consulta.html', {'form': form, 'mascota': mascota})


@staff_member_required
def editar_consulta(request, consulta_id):
    consulta = get_object_or_404(ConsultaVeterinaria, id=consulta_id)
    if request.method == 'POST':
        form = ConsultaVeterinariaForm(request.POST, instance=consulta)
        if form.is_valid():
            form.save()
            return redirect('detalle_mascota', mascota_id=consulta.mascota.id)
    else:
        form = ConsultaVeterinariaForm(instance=consulta)
    return render(request, 'veterinaria/editar_consulta.html', {'form': form, 'consulta': consulta})


@staff_member_required
def eliminar_consulta(request, consulta_id):
    consulta = get_object_or_404(ConsultaVeterinaria, id=consulta_id)
    if request.method == 'POST':
        mascota_id = consulta.mascota.id
        consulta.delete()
        return redirect('detalle_mascota', mascota_id=mascota_id)
    return render(request, 'veterinaria/eliminar_consulta.html', {'consulta': consulta})


@login_required
def detalle_vacunas(request, mascota_id):
    if request.user.is_staff:
        mascota = get_object_or_404(Mascota, id=mascota_id)
    else:
        mascota = get_object_or_404(Mascota, id=mascota_id, dueño=request.user)
    vacunas = mascota.vacunas.all()
    return render(request, 'veterinaria/detalle_vacunas.html', {'mascota': mascota, 'vacunas': vacunas})


@login_required
def detalle_consultas(request, mascota_id):
    if request.user.is_staff:
        mascota = get_object_or_404(Mascota, id=mascota_id)
    else:
        mascota = get_object_or_404(Mascota, id=mascota_id, dueño=request.user)
    consultas = mascota.consultas.all()
    return render(request, 'veterinaria/detalle_consultas.html', {'mascota': mascota, 'consultas': consultas})
