from django.shortcuts import redirect
from django.views import View

from apps.users.models import Usuario

class Inicio(View):
    def get(self, request):
        Usuario.crear_usuario_inicial()

        usuario = request.user
        if usuario.is_authenticated:
            return redirect(usuario.obtener_pagina_inicio())
        return redirect("usuarios:login")