from django.contrib.auth.forms import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from bosquetaoista.models import Grado, Casa, Persona, TipoDoc
from bosquetaoista.models import TipoEvento, Evento, Agenda, Cursante
from bosquetaoista.models import TipoExtra, PersonaExtra, TipoEstado, Frase
from django.utils.html import format_html

class LoginForm(forms.Form):
    username = forms.CharField(max_length = 65)
    password = forms.CharField(max_length = 65, 
						widget = forms.PasswordInput)

class RegistroForm(UserCreationForm):
	email = forms.EmailField()

	class Meta:
		model = User
		fields = ["username", 'first_name', 'last_name', "email", "password1", "password2", 'is_staff', 'is_superuser']


class GradoForm(forms.ModelForm):
	class Meta:
		model = Grado
		fields = ('id', 'nombre')
		labels = {'nombre':'Nombre'}

class CasaForm(forms.ModelForm):
	class Meta:
		model = Casa
		fields = ('nombre', 'direccion')
		labels = {
				'nombre':'Nombre',
				'direccion':'Dirección'
	    }

class TipoEstadoForm(forms.ModelForm):
	class Meta:
		model = TipoEstado
		fields = ('nombre',)
		labels = {'nombre':'Tipo de Estado'}


class TipoDocForm(forms.ModelForm):
	class Meta:
		model = TipoDoc
		fields = ('nombre', )
		labels = {'nombre':'Tipo de Documento'}

class PersonaForm(forms.ModelForm):
	class Meta:
		model = Persona
		fields = ('estado', 'orden', 'apellido', 'nombre', 
			'usuario', 'grado', 'casa_practica', 'responsable_casa', 
			'direccion', 'localidad', 'codigo_postal', 'email',
			'fechanacimiento', 'fechaingreso', 'fechaegreso',
			'celular', 'tipodoc', 'nrodoc', 'foto', 'certificado', )

		labels = {
				'estado':'Estado',
				'orden':'Orden',
				'apellido':'Apellido',
				'nombre':'Nombre',
				'usuario':'Usuario',
				'grado':'Grado',
				'casa_practica':'Casa de Práctica',
				'responsable_casa':'Responsable de Casa',
				'direccion':'Dirección',
				'localidad':'Localidad',
				'codigo_postal':'Código Postal',
				'email':'e-mail',
				'fechanacimiento':'Fecha de Nacimiento', 
				'fechaingreso':'Fecha Ingreso', 
				'fechaegreso':'Fecha Egreso',
				'celular':'Número de Celular', 
				'tipodoc':'Tipo de Documento`', 
				'nrodoc':'Número de Documento',
				'foto':'Foto',
				'certificado':'Certificado',
	    }

		widgets = {
			'estado': forms.Select(attrs={'style':'width:100px'}),
			'orden': forms.NumberInput(attrs={'style':'width:100px'}),
			'grado': forms.Select(attrs={'style':'width:200px'}),
			'casa_practica': forms.Select(attrs={'style':'width:200px'}),
			'responsable_casa': forms.Select(attrs={'style':'width:200px'}),
			'direccion': forms.TextInput(attrs={'style':'width:300px'}),
			'localidad': forms.TextInput(attrs={'style':'width:300px'}),
			'email': forms.EmailInput(attrs={'style':'width:300px'}),
			'tipodoc': forms.Select(attrs={'style':'width:100px'}),
		}

class TipoExtraForm(forms.ModelForm):
	class Meta:
		model = TipoExtra
		fields = {
			'nombre', 'descripcion', 
		}
		labels ={
			'nombre':'Nombre',
			'descripcion':'Descripción'
		}

class PersonaExtraForm(forms.ModelForm):
	class Meta:
		model = PersonaExtra
		fields = {
			'comentario', 'tipoextra', 
		}
		labels ={
			'tipoextra':'Extra',
			'comentario':'Comentario',
		}


class TipoEventoForm(forms.ModelForm):
	class Meta:
		model = TipoEvento
		fields = ('nombre', 'descripcion')
		labels = {
				'nombre':'Nombre',
				'descripcion':'Descripcion',
	    }

class EventoForm(forms.ModelForm):
	class Meta:
		model = Evento
		fields = ('tipo', 'nombre', 'descripcion')
		labels = {
				'tipo':'Tipo',
				'nombre':'Nombre',
				'descripcion':'Descripción'
	    }

class AgendaForm(forms.ModelForm):
	class Meta:
		model = Agenda
		fields = ('evento', 'fecha', 'orador')
		labels = {
				'evento':'Evento',
				'fecha':'Fecha',
				'orador':'Orador'
	    }

class CursanteForm(forms.ModelForm):
	class Meta:
		model = Cursante
		fields = ('agenda', 'persona', 'tipocursante')
		labels = {
				'agenda':'Agenda',
				'persona':'Persona',
				'estado':'Tipo de Cursante'
	    }


class FraseForm(forms.ModelForm):
	class Meta:
		model = Frase
		fields = ('id', 'frase', 'detalle')
		labels = {
				'id':'Id',
				'frase':'Frase',
				'detalle':'Detalle'
	    }
