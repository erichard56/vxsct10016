from django.contrib import admin
from bosquetaoista.models import Persona, Grado, Casa, \
	TipoEvento, Evento, Agenda, Cursante, TipoExtra, \
		PersonaExtra, TipoEstado, TipoDoc, Frase
from django.utils.html import format_html

# Register your models here.

class GradoAdmin(admin.ModelAdmin):
	list_display = ['nombre', ]

admin.site.register(Grado, GradoAdmin)

class CasaAdmin(admin.ModelAdmin):
	list_display = ['nombre', 'direccion', ]

admin.site.register(Casa, CasaAdmin)

class TipoEstadoAdmin(admin.ModelAdmin):
	list_display = ['nombre', ]

admin.site.register(TipoEstado, TipoEstadoAdmin)

class TipoDocAdmin(admin.ModelAdmin):
	list_display = ['nombre', ]

admin.site.register(TipoDoc, TipoDocAdmin)


class PersonaAdmin(admin.ModelAdmin):
	list_display = ['apellido', 'nombre', 'grado', 
	'usuario', 'casa_practica', 'responsable_casa', 'estado', ]

admin.site.register(Persona, PersonaAdmin)


class TipoExtraAdmin(admin.ModelAdmin):
	list_display = ['nombre', 'descripcion']

admin.site.register(TipoExtra, TipoExtraAdmin)


class PersonaExtraAdmin(admin.ModelAdmin):
	list_display = ['tipoextra', 'persona', 'comentario']

admin.site.register(PersonaExtra, PersonaExtraAdmin)


class TipoEventoAdmin(admin.ModelAdmin):
	list_display = ['nombre', ]

admin.site.register(TipoEvento, TipoEventoAdmin)

class EventoAdmin(admin.ModelAdmin):
	list_display = ['tipo', 'nombre', 'descripcion', ]

admin.site.register(Evento, EventoAdmin)

class AgendaAdmin(admin.ModelAdmin):
	list_display = ['evento', 'fecha', 'orador']

admin.site.register(Agenda, AgendaAdmin)

class CursanteAdmin(admin.ModelAdmin):
	list_display = ['agenda', 'persona', 'tipocursante']

admin.site.register(Cursante, CursanteAdmin)

class FraseAdmin(admin.ModelAdmin):
	list_display = ['id', 'frase', 'detalle']

admin.site.register(Frase, FraseAdmin)
