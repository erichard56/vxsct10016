from django.urls import path
from bosquetaoista.views import ingresar, registro, home, salir, cambiar_clave
from bosquetaoista.views import grados_lista, grado_am, grado_detalle
from bosquetaoista.views import casas_lista, casa_am, casa_detalle
from bosquetaoista.views import personas_lista, persona_am, \
    persona_detalle, persona_tipoextras_lista, persona_tipoextra_am, \
    persona_cambia_estado
from bosquetaoista.views import tipoextras_lista, tipoextra_am
from bosquetaoista.views import tipoeventos_lista, tipoevento_am
from bosquetaoista.views import eventos_lista, evento_am, evento_detalles
from bosquetaoista.views import agendas_lista, agenda_am, \
    agenda_cursantes, agenda_cursante_estado
from bosquetaoista.views import ayuda
from bosquetaoista.views import cargacsv, carga_frases

urlpatterns = [
    path('', ingresar, name = 'ingresar'),
    path('ingresar/', ingresar, name = 'ingresar'),
    path('cambiar_clave/', cambiar_clave, name = 'cambiar_clave'),
    path('registro/', registro, name = 'registro'),
    path('salir/', salir, name = 'salir'),
    path('home/', home, name = 'home'),
    path('grados_lista/', grados_lista, name = 'grados_lista'),
    path('grado_am/<int:id>', grado_am, name = 'grado_am'),
    path('grado_detalle/<int:id>', grado_detalle, name = 'grado_detalle'),
    path('casas_lista/', casas_lista, name = 'casas_lista'),
    path('casa_am/<int:id>', casa_am, name = 'casa_am'),
    path('casa_detalle/<int:id>', casa_detalle, name = 'casa_detalle'),
    path('personas_lista/<int:tipo>', personas_lista, name = 'personas_lista'),
    path('persona_am/<int:id>', persona_am, name = 'persona_am'),
    path('persona_detalle/<int:id>', persona_detalle, name = 'persona_detalle'),
    path('persona_tipoextras_lista/<int:id>', persona_tipoextras_lista, name = 'persona_tipoextras_lista'),
    path('persona_tipoextra_am/<int:exid>/<int:peid>', persona_tipoextra_am, name = 'persona_tipoextra_am'),
    path('persona_cambia_estado/<int:id>', persona_cambia_estado, name = 'persona_cambia_estado'),
    path('tipoextras_lista', tipoextras_lista, name = 'tipoextras_lista'),
    path('tipoextra_am/<int:id>', tipoextra_am, name = 'tipoextra_am'),
    path('tipoeventos_lista/', tipoeventos_lista, name = 'tipoeventos_lista'),
    path('tipoevento_am/<int:id>', tipoevento_am, name = 'tipoevento_am'),
    path('eventos_lista/', eventos_lista, name = 'eventos_lista'),
    path('evento_am/<int:id>', evento_am, name = 'evento_am'),
    path('evento_detalles/<int:id>', evento_detalles, name = 'evento_detalles'),
    path('agendas_lista/', agendas_lista, name = 'agendas_lista'),
    path('agenda_am/<int:id>', agenda_am, name = 'agenda_am'),
    path('agenda_cursantes/<int:id>', agenda_cursantes, name = 'agenda_cursantes'),
    path('agenda_cursante_estado/<int:agid>/<int:cuid>/<estado>', agenda_cursante_estado, name = 'agenda_cursante_estado'),
    path('ayuda', ayuda, name = 'ayuda'),

    path('cargacsv/<int:datos>', cargacsv, name = 'cargacsv'),
    path('carga_frases/<int:flag>', carga_frases, name = 'carga_frases'),
]

