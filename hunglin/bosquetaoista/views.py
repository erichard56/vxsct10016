from django.shortcuts import render, redirect
import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth import update_session_auth_hash
import base64
from django.conf.urls.static import static
from django.contrib.auth.forms import PasswordChangeForm
from django.db.models import Max, Q
import random
from bosquetaoista.models import Grado, Casa, Persona, \
	TipoEvento, Evento, Agenda, Cursante, PersonaExtra, \
	TipoExtra, TipoEstado, TipoDoc, TipoCursante, Frase
from bosquetaoista.forms import GradoForm, CasaForm, PersonaForm, \
	TipoEventoForm, EventoForm, AgendaForm, TipoExtraForm, \
	PersonaExtraForm, LoginForm, RegistroForm, TipoDocForm, TipoEstadoForm

def inicializar_bd():
	# Tipo de Documento
	cant = TipoDoc.objects.all().count()
	if (not cant):
		for item in ['DNI', 'CI', 'PASAPORTE']:
			tipodoc = TipoDoc()
			tipodoc.nombre = item
			tipodoc.save()
	# Tipo de Estado de la Persona
	cant = TipoEstado.objects.all().count()
	if (not cant):
		for item in ['Activo', 'No Activo', 'Fallecido']:
			instancia = TipoEstado()
			instancia.nombre = item
			instancia.save()
	# Tipo de estado del cursante
	ntcantcu = TipoCursante.objects.all().count()
	if (not cant):
		for item in ['Anotado', 'Finalizado', 'No Finalizado']:
			instancia = TipoCursante()
			instancia.nombre = item
			instancia.save()
	# TipoEventos
	cant = TipoEvento.objects.all().count()
	if (not cant):
		for item in ['Cursos', 'Actividades', 'Prácticas']:
			instancia = TipoEvento()
			instancia.nombre = item
			instancia.descripcion = item
			instancia.save()
	# Grados
	cant = Grado.objects.all().count()
	if (not cant):
		for item in ['Maestro', 'Instructor', 'Alumno']:
			instancia = Grado()
			instancia.nombre = item
			instancia.save()
	return


def ingresar(request):
	if (request.method == 'GET'):
		if (request.user.is_authenticated):
			return(redirect('/home/'))

		form = LoginForm()
		return(render(request, 'login.html', {'form':form}))

	elif request.method == 'POST':
		form = LoginForm(request.POST)
        			
		if (form.is_valid()):
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			user = authenticate(request, username=username, password=password)
			if (user):
				login(request, user)
				inicializar_bd()
				return redirect('/home/')
		messages.error(request,f'Usuario o Clave inválido')
		return(render(request,'login.html', {'form':form}))


@login_required
def cambiar_clave(request):
	if request.method == 'POST':
		form = PasswordChangeForm(request.user, request.POST)
		if form.is_valid():
			user = form.save()
			update_session_auth_hash(request, user)  # Important!
			messages.success(request, 'Clave modificada!')
			return redirect('home')
		else:
			messages.error(request, 'Error detectado.')
	else:
		form = PasswordChangeForm(request.user)
	ctx = { 'form':form }
	return render(request, 'cambiar_clave.html', ctx)


@login_required
def registro(request):
	if request.method == "GET":
		form = RegistroForm()

	elif request.method == "POST":
		form = RegistroForm(request.POST)
		if form.is_valid():
			n = User.objects.filter(email=request.POST['email']).count()
			if (n == 0):
				tipoestado = TipoEstado.objects.get(nombre='Activo')
				tipodoc = TipoDoc.objects.get(nombre='DNI')
				if (tipoestado and tipodoc):
					form.save()
					persona = Persona.objects.get(email=request.POST['email'])
					if (not persona):
						persona.orden = get_next_orden(0, 0)
						persona.nombre = request.POST['first_name']
						persona.apellido = request.POST['last_name']
						persona.email = request.POST['email']
						persona.estado_id = tipoestado.id
						persona.tipodoc_id = tipodoc.id
					persona.usuario = request.POST['username']
					persona.save()
					return redirect("/home")
				else:
					messages.error(request,f'Debe existir Activo (como Estado) y DNI (como Documento)')
					return redirect("/registro")
			else:
				messages.error(request,f'Error mail ya utilizado')
				return redirect("/registro")
		else:
			messages.error(request,f'Error agregando usuario nuevo')
			for e in form.errors:
				messages.error(request, f'error {e}')
			return redirect("/registro")
	return render(request, "registro.html", {"form":form})


def ayuda(request):
	return (render(request, 'ayuda.html'))


def salir(request):
	logout(request)
	return redirect('/ingresar/')


@login_required
def home(request):
	nid = random.randint(1, 110)
	frase = Frase.objects.get(pk = nid)
	ctx = { 'pagina':1, 'frase':frase }
	return(render(request, 'home.html', ctx))


# Grados
@login_required
def grados_lista(request):
	grados = []
	activo = TipoEstado.objects.get(nombre='Activo')
	noactivo = TipoEstado.objects.get(nombre='No Activo')
	todos = Grado.objects.all().order_by('id')
	for grado in todos:
		activos = Persona.objects.filter(grado_id=grado.id).filter(estado_id=activo.id).count()
		if (not activos):
			activos = 0
		noactivos = Persona.objects.filter(grado_id=grado.id).filter(estado_id=noactivo.id).count()
		if (not noactivos):
			noactivos = 0
		grados.append([grado.id, grado.nombre, activos, noactivos])
	ctx = { 'pagina':2, 'grados':grados }
	return(render(request, 'grados_lista.html', ctx))


@login_required
def grado_am(request, id):

	if (request.method == 'GET'):
		if (id == 0):
			form = GradoForm()
			titulo = 'Nuevo Grado'
		else:
			grado = Grado.objects.get(pk = id)
			form = GradoForm(instance=grado)
			titulo = f'Modificacion Grado'
		ctx = { 'pagina':2, 'titulo':titulo, 'form':form }
		return(render(request, 'general_am.html', ctx))

	elif (request.method == 'POST'):
		form = GradoForm(request.POST, request.FILES)
		if (form.is_valid()):
			if (id == 0):
				form.save()
			else:
				grado = Grado.objects.get(pk = id)
				grado.nombre = request.POST['nombre']
				grado.save()
		else:
			messages.error(request,f'Formulario con erroes')
			for e in form.errors:
				messages.error(request, f'error {e}')
	return(redirect('grados_lista'))


# Grados
@login_required
def grado_detalle(request, id):
	grado = Grado.objects.get(pk=id)
	personas = Persona.objects.filter(grado_id=id).filter(estado__nombre='Activo').order_by('orden')
	ctx = { 'pagina':2, 'grado':grado, 'personas':personas, 'pedirfoto':'pedir' }
	return(render(request, 'grado_detalle.html', ctx))


# Casas
@login_required
def casas_lista(request):
	todos = []
	casas = Casa.objects.all().order_by('id')
	for casa in casas:
		personas = Persona.objects.filter(responsable_casa=casa.id)
		responsable = ''
		if (personas):
			for persona in personas:
				if (len(responsable) > 0):
					responsable = responsable + ' // ' + persona.apellido + ', ' + persona.nombre
				else:
					responsable = responsable + persona.apellido + ', ' + persona.nombre
		else:
			resp = ''
		qactivos = Persona.objects.filter(casa_practica_id=casa.id).filter(estado__nombre='Activo').count()
		qnoactivos = Persona.objects.filter(casa_practica_id=casa.id).filter(estado__nombre='No Activo').count()
		qfallecidos = Persona.objects.filter(casa_practica_id=casa.id).filter(estado__nombre='Fallecido').count()
		todos.append([casa.id, casa.nombre, casa.direccion, responsable, 
						qactivos, qnoactivos, qfallecidos])
	ctx = { 'pagina':4, 'casas':todos }
	return(render(request, 'casas_lista.html', ctx))


@login_required
def casa_am(request, id):

	if (request.method == 'GET'):
		if (id == 0):
			form = CasaForm()
			titulo = 'Nueva Casa'
		else:
			casa = Casa.objects.get(pk = id)
			form = CasaForm(instance=casa )
			titulo = f'Modificacion Casa'

		ctx = { 'pagina':4, 'titulo':titulo, 'form':form }
		return(render(request, 'general_am.html', ctx))

	elif (request.method == 'POST'):
		form = CasaForm(request.POST, request.FILES)
		if (form.is_valid()):
			if (id == 0):
				form.save()
			else:
				casa = Casa.objects.get(pk = id)
				casa.nombre = request.POST['nombre']
				casa.direccion = request.POST['direccion']
				casa.save()
		else:
			for e in form.errors:
				messages.error(request, f'error {e}')
	return(redirect('casas_lista'))


@login_required
def casa_detalle(request, id):
	casa = Casa.objects.get(pk=id)
	personas = Persona.objects.filter(casa_practica_id=id).order_by('casa_practica', 'orden')
	responsables = Persona.objects.filter(responsable_casa_id=id)
	ctx = { 'pagina':4, 'casa':casa, 'responsables':responsables, 'personas':personas }
	return(render(request, 'casa_detalle.html', ctx))


# Personas
@login_required
def personas_lista(request, tipo):
	estados = TipoEstado.objects.all().order_by('nombre')
	if (request.user.is_superuser):
		# si es superuser puede ver todo
		yosoy = None
		tipoestado = TipoEstado.objects.get(nombre='Activo')
		if (tipo == 0):
			todos = Persona.objects.all().order_by('estado', 'orden') 
		elif (tipo == 1):
			todos = Persona.objects.filter(estado=tipoestado.id).order_by('estado', 'orden') 
		else:
			todos = Persona.objects.exclude(estado=tipoestado.id).order_by('estado', 'orden') 

	elif (request.user.is_staff):
		'''
			si no es superuser, pero es staff, averiguo si es responsable de casa. 
			si es responsable de casa, muestro a todas las personas de esa casa
			si no es responsable de casa, no muestro nada
		'''
		yosoy = Persona.objects.filter(usuario=request.user.username).first()
		if (yosoy):
			if (yosoy.responsable_casa):
				todos = Persona.objects.filter(casa_practica=yosoy.responsable_casa_id).order_by('estado', 'orden') 
			else:
				todos = None
		else:
			messages.error(request, f'No es usuario')
			return(redirect('home'))
	else:
		messages.error(request, f'Debe ser superuser o staff')
		return(redirect('home'))

	if (request.method == 'POST'):
		estado_id = int(request.POST['estado'])
		busq = request.POST['busca']
		if (busq):
			todos = Persona.objects.filter(Q(apellido__icontains=busq) | Q(nombre__icontains=busq)) 
		else:
			if (estado_id == 0):
				todos = Persona.objects.all().order_by('orden') 
			else:
				todos = Persona.objects.filter(estado_id=estado_id).order_by('orden') 

	personas = []
	foto = None
	for todo in todos:
	#	if (todo.foto):
	#		foto = base64.b64encode(todo.foto).decode()
	#	else:
	#	 	foto = None
		personas.append([todo, foto])
	ctx = { 'pagina':6, 'yosoy':yosoy, 'personas':personas, 'estados':estados }
	return(render(request, 'personas_lista.html', ctx))


def convert_fecha(fecha):
	if (fecha):
		f = fecha.split('/')
		if (len(f) == 3):
			return(datetime.datetime(int(f[2]), int(f[1]), int(f[0])))
		elif (len(f) == 2):
			return(datetime.datetime(int(f[1]), int(f[0]), 1))
		else:
			return(datetime.datetime(int(f[0]), 1, 1))
	else:
		return(None)


def get_next_orden(id, porden):
	if (id == 0):
		cantidad = Persona.objects.count()
		if (cantidad == 0):
			orden = 1
		else:
			orden = Persona.objects.aggregate(Max('orden'))['orden__max']
			orden = orden + 1
	else:
		if (int(porden) == 0):
			orden = Persona.objects.aggregate(Max('orden'))['orden__max'] + 1
		else:
			cantidad = Persona.objects.filter(orden=porden).exclude(id=id).count()
			if (cantidad == 0):
				orden = int(porden)
			else:
				orden = 0
	return(orden)


@login_required
def persona_am(request, id):
	if (request.method == 'GET'):
		if (id == 0):
			form = PersonaForm()
			titulo = 'Nueva Persona'
			foto = ''
		else:
			persona = Persona.objects.get(pk = id)
			form = PersonaForm(instance=persona)
			titulo = f'Modificación Persona'
			foto = None
		ctx = { 'pagina':6, 'titulo':titulo, 'form':form, 'persona':persona, 'pedirfoto':'pedirfoto' }
		return(render(request, 'persona_am.html', ctx))

	elif (request.method == 'POST'):
		form = PersonaForm(data=request.POST, files=request.FILES)
		if (True):			# (form.is_valid()):
			if (id == 0):
				persona = Persona()
			else:
				persona = Persona.objects.get(pk = id)
			if (request.POST['apellido'] == 'Durán Agra'):
				persona.orden = 0
			else:
				persona.orden = get_next_orden(id, request.POST['orden'])
				if (persona.orden == -1):
					messages.error(request, f'Numero de Orden {request.POST["orden"]} ya utilizado')
					return(redirect('/persona_am/' + str(id)))

			persona.nombre = request.POST['nombre']
			persona.apellido = request.POST['apellido']
			persona.usuario = request.POST['usuario']
			persona.grado_id = request.POST['grado']
			persona.casa_practica_id = request.POST['casa_practica']
			persona.responsable_casa_id = request.POST['responsable_casa']
			persona.estado_id = request.POST['estado']
			persona.direccion = request.POST['direccion']
			persona.localidad = request.POST['localidad']
			persona.codigo_postal = request.POST['codigo_postal']
			persona.email = request.POST['email']
			persona.fechanacimiento = convert_fecha(request.POST['fechanacimiento'])
			persona.fechaingreso = convert_fecha(request.POST['fechaingreso'])
			persona.fechaegreso = convert_fecha(request.POST['fechaegreso'])
			persona.celular = request.POST['celular']
			persona.tipodoc_id = request.POST['tipodoc']
			nrodoc = request.POST['nrodoc']
			if (nrodoc):
				persona.nrodoc = nrodoc
			#foto = request.FILES.get('photo', False)
			#if (foto):
			#	if (persona.foto):
			#		max_size = 200 * 1014 * 1024
			#		if (len(persona.foto) > max_size):
			#			messages.error(request, f'Foto demasiado grande ({len(persona.foto)}), Máximo {max_size}.')
			#			return(redirect('/persona_am/' + str(id)))
			foto = request.FILES.get('foto',False)
			if (foto):
				persona.foto = request.FILES['foto']
			certificado = request.FILES.get('certificado',False)
			if (certificado):
				persona.certificado = request.FILES['certificado']
			persona.save()
		else:
			for e in form.errors:
				messages.error(request, f'error {e}')
			return(redirect('/persona_am/' + str(id)))
	return(redirect('/personas_lista/1'))


@login_required
def persona_detalle(request, id):
	persona = Persona.objects.get(pk = id)
	cursantes = Cursante.objects.filter(persona_id = id).order_by('tipocursante__nombre')
	personaextras = PersonaExtra.objects.filter(persona_id = id).order_by('tipoextra__nombre')
	ctx = { 'pagina':6, 'persona':persona, 'cursantes':cursantes, 'personaextras':personaextras }
	return(render(request, 'persona_detalle.html', ctx))


@login_required
def persona_tipoextras_lista(request, id):
	persona = Persona.objects.get(pk=id)
	personaextras = PersonaExtra.objects.filter(persona_id=id)
	ctx = { 'pagina':16,  'persona':persona, 
			'personaextras':personaextras }
	return(render(request, 'persona_tipoextras_lista.html', ctx))


@login_required
def persona_tipoextra_am(request, exid, peid):

	if (request.method == 'GET'):
		if (exid == 0):
			form = PersonaExtraForm()
			titulo = 'Nueva Info Extra'
		else:
			personaextras = PersonaExtra.objects.filter(persona_id=peid).filter(tipoextra_id=exid)
			form = PersonaExtraForm(instance=personaextras[0])
			titulo = f'Modificacion Info Extra)' 
		ctx = { 'pagina':17, 'titulo':titulo, 'form':form,
				'personaextras':'personaextras'
		}
		return(render(request, 'general_am.html', ctx))

	elif (request.method == 'POST'):
		form = PersonaExtraForm(request.POST, request.FILES)
		if (form.is_valid()):
			if (exid == 0):
				personaextra = PersonaExtra()
				personaextra.persona_id = peid
			else:
				personaextras = PersonaExtra.objects.filter(tipoextra_id=exid).filter(persona_id=peid)
				personaextra = personaextras[0]

			personaextra.tipoextra_id = request.POST['tipoextra']
			personaextra.persona_id = peid
			personaextra.comentario = request.POST['comentario']
			personaextra.save()
		else:
			for e in form.errors:
				messages.error(request, f'error {e}')
	return(redirect('/persona_tipoextras_lista/' + str(peid)))

@login_required
def persona_cambia_estado(request, id):
	activo = TipoEstado.objects.get(nombre='Activo')
	noactivo = TipoEstado.objects.get(nombre='No Activo')
	persona = Persona.objects.get(id=id)
	if (persona.estado_id == noactivo.id):
		persona.estado_id = activo.id
	else:
		persona.estado_id = noactivo.id
	persona.save()
	return(redirect('/personas_lista/0'))

# extra
@login_required
def tipoextras_lista(request):
	tipoextras = TipoExtra.objects.all().order_by('id')
	ctx = { 'pagina':14, 'tipoextras':tipoextras }
	return(render(request, 'tipoextras_lista.html', ctx))


@login_required
def tipoextra_am(request, id):

	if (request.method == 'GET'):
		if (id == 0):
			form = TipoExtraForm()
			titulo = 'Nuevo Tipo de Información Extra'
		else:
			tipoextra = TipoExtra.objects.get(pk = id)
			form = TipoExtraForm(instance=tipoextra)
			titulo = f'Modificacion de Tipo Extra' 
		ctx = { 'pagina':14, 'titulo':titulo, 'form':form }
		return(render(request, 'general_am.html', ctx))

	elif (request.method == 'POST'):
		form = TipoExtraForm(request.POST, request.FILES)
		if (form.is_valid()):
			if (id == 0):
				form.save()
			else:
				tipoextra = TipoExtra.objects.get(pk = id)
				tipoextra.nombre = request.POST['nombre']
				tipoextra.descripcion = request.POST['descripcion']
				tipoextra.save()
		else:
			for e in form.errors:
				messages.error(request, f'error {e}')
	return(redirect('tipoextras_lista'))


# Tipos de Eventos --> Cursos, Actividades, Prácticas
@login_required
def tipoeventos_lista(request):
	tipoeventos = TipoEvento.objects.all().order_by('id')
	ctx = { 'pagina':12, 'tipoeventos':tipoeventos }
	return(render(request, 'tipoeventos_lista.html', ctx))


@login_required
def tipoevento_am(request, id):

	if (request.method == 'GET'):
		if (id == 0):
			form = TipoEventoForm()
			titulo = 'Nuevo Tipo de Evento'
		else:
			evento = TipoEvento.objects.get(pk = id)
			form = TipoEventoForm(instance=evento)
			titulo = f'Modificacion Tipo de Evento' 
		ctx = { 'pagina':12, 'titulo':titulo, 'form':form }
		return(render(request, 'general_am.html', ctx))

	elif (request.method == 'POST'):
		form = TipoEventoForm(request.POST, request.FILES)
		if (form.is_valid()):
			if (id == 0):
				form.save()
			else:
				tipoevento = TipoEvento.objects.get(pk = id)
				tipoevento.nombre = request.POST['nombre']
				tipoevento.descripcion = request.POST['descripcion']
				tipoevento.save()
		else:
			for e in form.errors:
				messages.error(request, f'error {e}')
	return(redirect('tipoeventos_lista'))


# Eventos
@login_required
def eventos_lista(request):
	eventos = Evento.objects.all().order_by('id')
	ctx = { 'pagina':8, 'eventos':eventos }
	return(render(request, 'eventos_lista.html', ctx))


@login_required
def evento_am(request, id):

	if (request.method == 'GET'):
		if (id == 0):
			form = EventoForm()
			titulo = 'Nuevo Evento'
		else:
			evento = Evento.objects.get(pk = id)
			form = EventoForm(instance=evento)
			titulo = f'Modificacion Evento' 
		ctx = { 'pagina':9, 'titulo':titulo, 'form':form }
		return(render(request, 'general_am.html', ctx))

	elif (request.method == 'POST'):
		form = EventoForm(request.POST, request.FILES)
		if (form.is_valid()):
			if (id == 0):
				form.save()
			else:
				evento = Evento.objects.get(pk = id)
				evento.tipo_id = request.POST['tipo']
				evento.nombre = request.POST['nombre']
				evento.descripcion = request.POST['descripcion']
				evento.save()
		else:
			for e in form.errors:
				messages.error(request, f'error {e}')
	return(redirect('eventos_lista'))


@login_required
def evento_detalles(request, id):
	evento = Evento.objects.get(pk=id)
	agendas = Agenda.objects.filter(evento_id=id).order_by('-fecha')
	todos = []
	for agenda in agendas:
		cursantes = Cursante.objects.filter(agenda_id=agenda.id).order_by('persona_id__apellido', 'tipocursante_id__nombre')
		todos.append([agenda, cursantes])
	ctx = { 'pagina':8, 'evento':evento, 'todos':todos }
	return(render(request, 'evento_detalles.html', ctx))

# Agenda de Eventos
@login_required
def agendas_lista(request):
	agendas = Agenda.objects.all().order_by('fecha')
	ctx = { 'pagina':10, 'agendas':agendas }
	return(render(request, 'agendas_lista.html', ctx))


@login_required
def agenda_am(request, id):

	if (request.method == 'GET'):
		if (id == 0):
			form = AgendaForm()
			titulo = 'Nueva Agenda'
		else:
			agenda = Agenda.objects.get(pk = id)
			form = AgendaForm(instance=agenda)
			titulo = f'Modificacion Agenda' 
		ctx = { 'pagina':11, 'titulo':titulo, 'form':form }
		return(render(request, 'general_am.html', ctx))

	elif (request.method == 'POST'):
		form = AgendaForm(request.POST, request.FILES)
		if (form.is_valid()):
			if (id == 0):
				form.save()
			else:
				agenda = Agenda.objects.get(pk = id)
				agenda.evento_id = request.POST['evento']
				agenda.fecha = convert_fecha(request.POST['fecha'])
				agenda.orador_id = request.POST['orador']
				agenda.save()
		else:
			for e in form.errors:
				messages.error(request, f'error {e}')
	return(redirect('agendas_lista'))


@login_required
def agenda_cursantes(request, id):
	agenda = Agenda.objects.get(pk=id)
	cursantes = []
	idss = []
	curs = Cursante.objects.filter(agenda_id=id).order_by('tipocursante','persona__apellido')
	for cur in curs:
		cursantes.append([cur.persona.id, cur.tipocursante.nombre, cur.persona.apellido,
			cur.persona.nombre, cur.persona.casa_practica, id, cur.persona_id])
		idss.append(cur.persona.id)
	tipoestado = TipoEstado.objects.get(nombre='Activo')
	personas = Persona.objects.filter(estado_id=tipoestado.id).exclude(id__in=idss).order_by('apellido')
	for persona in personas:
		cursantes.append([0, '??', persona.apellido,
			persona.nombre, persona.casa_practica, id, persona.id])
	ctx = { 'pagina':10, 'cursantes':cursantes, 'agenda':agenda }
	return(render(request, 'agenda_cursantes.html', ctx))


@login_required
def agenda_cursante_estado(request, agid, cuid, estado):
	if (estado == 'Eliminar'):
		cursantes = Cursante.objects.filter(agenda_id = agid, persona_id=cuid)
		if (cursantes):
			cursantes.delete()
	else:
		cursantes = Cursante.objects.filter(agenda_id = agid, persona_id=cuid)
		if (cursantes):
			cursante = cursantes[0]
		else:
			cursante = Cursante()
			cursante.agenda_id = agid
			cursante.persona_id = cuid
		tipocursante = TipoCursante.objects.get(nombre=estado)
		cursante.tipocursante_id = tipocursante.id
		cursante.save()
	return(redirect('/agenda_cursantes' + '/' + str(agid)))

def corrige_fecha(f):
	if (f.find(' ') >= 0):
		f = f.replace(' ', '/')
	elif (f.find('-') >= 0):
		f = f.replace('-', '/')
	f = f.replace('ene', '01')
	f = f.replace('feb', '02')
	f = f.replace('mar', '03')
	f = f.replace('abr.', '04')
	f = f.replace('abr', '04')
	f = f.replace('may.', '05')
	f = f.replace('may', '05')
	f = f.replace('jun', '06')
	f = f.replace('jul', '07')
	f = f.replace('ago', '08')
	f = f.replace('sept.', '09')
	f = f.replace('sep', '09')
	f = f.replace('oct', '10')
	f = f.replace('nov', '11')
	f = f.replace('dic', '12')
	fecha = convert_fecha(f)
	return(fecha)

@login_required
def cargacsv(request, datos):
	file1 = open('../Alumnos_Bosque_Taoista.csv', 'r')
	Lines = file1.readlines()

# [0]: NumerodeOrden	[1]: Marcatemporal		[2]: Activo
# [3]: FechadeIngreso	[4]: FechadeEgreso		[5]: Apellidos,
# [6]: Nombres			[7]: FechadeNacimiento	[8]: NumerodeCelular
# [9]: TipodeDocumento	[10]: NumerodeDocumento	[11]: e-mail,
# [12]: Sededepracticaalaquepertenece	[13]: Direccion
# [14]: Localidad		[15] CodigoPostal		[16] OtroTelefono
# [17]: ¿Realizaalgunapracticamarcialprevia?	[18] ¿Cual?
# [19]: ¿Poseecertificadomedico?
# [20]: Describecualquierotrodatoqueteparezcarelevante,
# [21]: Decinoscomonosconociste		[22]: InstructorPadre
# [23]: Cursosaprobados		[24]: Otrasactividades
# [25]: SeudonimoChino		[26]: TraducciondelSeudonimo	
# [27]: Imagendelseudonimo

	n = len(Lines)
	i = 1
	while (i < n):
		regi = Lines[i]
		i = i + 1
		for j in range(i, n):
			regj = Lines[j].split(';')
			if (regj[0].isnumeric()):
				break
			else:
				regi = regi + Lines[j]
				i = i + 1

		reg = regi.split(';')
		activo = TipoEstado.objects.get(nombre='Activo')
		noactivo = TipoEstado.objects.get(nombre='No Activo')
		tipodoc = TipoDoc.objects.get(nombre='DNI')
		grado = Grado.objects.get(nombre='Alumno')
		nn = Persona.objects.filter(orden=int(reg[0])).count()
		if (nn == 0):
			persona = Persona()
		else:
			persona = Persona.objects.get(orden=int(reg[0]))
		if (datos == 0):
			persona.orden = reg[0]
			persona.nombre = reg[6]
			persona.apellido = reg[5]
			persona.usuario = ''
			persona.grado_id = grado.id
			persona.casa_practica_id = ''
			persona.responsable_casa_id = ''
			if (reg[2] == 'Si'):
				persona.estado_id = activo.id
			else:
				persona.estado_id = noactivo.id
			persona.direccion = reg[13]
			persona.localidad = reg[14]
			persona.codigo_postal = reg[15]
			if (reg[11].count('@') == 1):
				persona.email = reg[11]
			else:
				persona.email = ''
			fecha = corrige_fecha(reg[7])
			persona.fechanacimiento = fecha
			fecha = corrige_fecha(reg[3])
			persona.fechaingreso = fecha
			fecha = corrige_fecha(reg[4])
			persona.fechaegreso = fecha
			persona.celular = reg[8]
			persona.tipodoc_id = tipodoc.id
			if (reg[10].isnumeric()):
				persona.nrodoc = int(reg[10])
			else:
				persona.nrodoc = 0
			persona.save()

		elif (datos == 1):
			persona = Persona.objects.get(orden=int(reg[0]))

			# [17]: ¿Realizaalgunapracticamarcialprevia?	[18] ¿Cual?
			if (reg[17] == 'Si'):
				extraid = 2
				nn = PersonaExtra.objects.filter(persona_id=persona.id, tipoextra_id=extraid).count()
				if (nn == 0):
					extra = PersonaExtra()
					extra.comentario = reg[18]
					extra.persona_id = persona.id
					extra.tipoextra_id = extraid
					extra.save()
	
			# [19]: ¿Poseecertificadomedico?
				extraid = 6
				nn = PersonaExtra.objects.filter(persona_id=persona.id, tipoextra_id=extraid).count()
				if (nn == 0):
					extra = PersonaExtra()
					extra.comentario = reg[19]
					extra.persona_id = persona.id
					extra.tipoextra_id = extraid
					extra.save()

			# [20]: Describecualquierotrodatoqueteparezcarelevante
			if (reg[20]):
				extraid = 3
				nn = PersonaExtra.objects.filter(persona_id=persona.id, tipoextra_id=extraid).count()
				if (nn == 0):
					extra = PersonaExtra()
					extra.comentario = reg[20]
					extra.persona_id = persona.id
					extra.tipoextra_id = extraid
					extra.save()

			# [21]: Decinoscomonosconociste
			if (reg[21]):
				extraid = 4
				nn = PersonaExtra.objects.filter(persona_id=persona.id, tipoextra_id=extraid).count()
				if (nn == 0):
					extra = PersonaExtra()
					extra.comentario = reg[21]
					extra.persona_id = persona.id
					extra.tipoextra_id = extraid
					extra.save()

			# [22]: InstructorPadre
			if (reg[22]):
				extraid = 5
				nn = PersonaExtra.objects.filter(persona_id=persona.id, tipoextra_id=extraid).count()
				if (nn == 0):
					extra = PersonaExtra()
					extra.comentario = reg[22]
					extra.persona_id = persona.id
					extra.tipoextra_id = extraid
					extra.save()
			
			# [23]: Cursos Aprobados (Historico)
			if (reg[23]):
				extraid = 7
				if (nn == 0):
					extra = PersonaExtra()
					extra.comentario = reg[23]
					extra.persona_id = persona.id
					extra.tipoextra_id = extraid
					extra.save()

			# [24]: Otras Actividades (Historico)
			if (reg[24]):
				extraid = 8
				nn = PersonaExtra.objects.filter(persona_id=persona.id, tipoextra_id=extraid).count()
				if (nn == 0):
					extra = PersonaExtra()
					extra.comentario = reg[24]
					extra.persona_id = persona.id
					extra.tipoextra_id = extraid
					extra.save()

			# [25]: SeudonimoChino		[26]: TraducciondelSeudonimo
			if (reg[25]):
				extraid = 1
				nn = PersonaExtra.objects.filter(persona_id=persona.id, tipoextra_id=extraid).count()
				if (nn == 0):
					extra = PersonaExtra()
					extra.comentario = reg[25] + '(' + reg[26] + ')'
					extra.persona_id = persona.id
					extra.tipoextra_id = extraid
					extra.save()

		else:
			pass

	return(redirect('/personas_lista/1'))

def limpia(s):
	t = s.replace('Ã¡', 'á').replace('Ã©', 'é').replace('Ã­', 'í').replace('Ã³', 'ó').replace('Ãº', 'ú').replace('Ã±', 'ñ')
	return(t)

@login_required
def carga_frases(request, flag):
	file1 = open('../frases.txt', 'r')
	Lines = file1.readlines()

# 1. La mejor victoria es vencer sin combatir.
# Si somos lo suficientemente inteligentes no deberemos combatir para salir airosos de un problema.

# 2. Si utilizas al enemigo para derrotar al enemigo, serás poderoso en cualquier lugar a donde vayas.
# Saber enemistar a terceros nos puede hacer alcanzar la victoria sin mover ni un solo dedo.

# 3. Llévalos a un punto del que no puedan salir, y morirán antes de poder escapar.
# En esta cita, Sun Tzu nos habla sobre la importancia de rodear a nuestros enemigos.

	Frase.objects.all().delete()

	n = len(Lines)
	i = 0
	while (i < n):
		regi = Lines[i]
		if ('0' <= regi[0] and regi[0] <= '9'):
			regi = regi.split('.')
			nid = int(regi[0])
			regi1 = limpia(regi[1].strip())
			i += 1
			regi2 = limpia(Lines[i].strip())
			print(f'_{nid}_{regi1}_{regi2}_{n}_')
			frase = Frase()
			frase.id = nid
			frase.frase = regi1
			frase.detalle = regi2
			frase.save()
		else:
			i += 1

	return(redirect('/personas_lista/1'))

