from django.contrib import messages

class MensajeMixin(object):
    mensaje_exito = "¡La información se ha guardado exitosamente!"
    mensaje_error = "¡El formulario tiene errores, por favor revise la información!"

    def form_valid(self, form):
        messages.success(self.request, self.mensaje_exito)
        return super(MensajeMixin, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, self.mensaje_error)
        return super(MensajeMixin, self).form_invalid(form)