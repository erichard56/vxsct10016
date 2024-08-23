from django.db import models

# Create your models here.

class Grado(models.Model):
	nombre = models.CharField(max_length=200)

	def __str__(self):
		return(self.nombre)

class Casa(models.Model):
	nombre = models.CharField(max_length=200)
	direccion = models.CharField(max_length=200)

	def __str__(self):
		return(self.nombre)

class TipoEstado(models.Model):
	nombre = models.CharField(max_length=20)

	def __str__(self):
		return(self.nombre)

class TipoDoc(models.Model):
	nombre = models.CharField(max_length=20)

	def __str__(self):
		return(self.nombre)

class Persona(models.Model):
	orden = models.IntegerField(default=0)
	nombre = models.CharField(max_length=50)
	apellido = models.CharField(max_length=50)
	usuario = models.CharField(max_length=50, blank=True)
	grado = models.ForeignKey(Grado, on_delete=models.CASCADE, null=True)
	casa_practica = models.ForeignKey(Casa, on_delete=models.CASCADE, 
		related_name='casa_practica', null=True)
	responsable_casa = models.ForeignKey(Casa, on_delete=models.CASCADE, 
		related_name='responsable_casa', null=True, blank=True)
	estado = models.ForeignKey(TipoEstado, on_delete=models.CASCADE)
	direccion = models.CharField(max_length=50, blank=True)
	localidad = models.CharField(max_length=50, blank=True)
	codigo_postal = models.CharField(max_length=10, blank=True)
	email = models.EmailField(max_length=50, blank=True)
	fechanacimiento = models.DateField(blank=True, null=True)
	fechaingreso = models.DateField(blank=True, null=True)
	fechaegreso = models.DateField(blank=True, null=True)
	celular = models.CharField(max_length=50, blank=True)
	tipodoc = models.ForeignKey(TipoDoc, on_delete=models.CASCADE)
	nrodoc = models.IntegerField(blank=True, default=0)
	foto = models.ImageField(upload_to='images/', null=True)

	def __str__(self):
		return(self.apellido + ', ' + self.nombre)


class TipoExtra(models.Model):
	nombre = models.CharField(max_length=20)
	descripcion = models.CharField(max_length=200)

	def __str__(self):
		return(self.nombre)

class PersonaExtra(models.Model):
	tipoextra = models.ForeignKey(TipoExtra, on_delete=models.CASCADE)
	persona = models.ForeignKey(Persona, on_delete=models.CASCADE)
	comentario = models.CharField(max_length=1000)

class TipoEvento(models.Model):
	nombre = models.CharField(max_length=20)
	descripcion = models.CharField(max_length=200)

	def __str__(self):
		return(self.nombre)

class Evento(models.Model):
	tipo = models.ForeignKey(TipoEvento, on_delete=models.CASCADE)
	nombre = models.CharField(max_length=30)
	descripcion = models.CharField(max_length=200)

	def __str__(self):
		return(self.nombre)

class Agenda(models.Model):
	evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
	fecha = models.DateField()
	orador = models.ForeignKey(Persona, 
		limit_choices_to = {'estado_id':1},
		on_delete=models.CASCADE)

	def __str__(self):
		return(f'{self.evento} - {self.fecha:%d-%m-%y}')

class TipoCursante(models.Model):
	nombre = models.CharField(max_length=20)

	def __str__(self):
		return(self.nombre)

class Cursante(models.Model):
	agenda = models.ForeignKey(Agenda, on_delete=models.CASCADE)
	persona = models.ForeignKey(Persona, on_delete=models.CASCADE)
	tipocursante = models.ForeignKey(TipoCursante, on_delete=models.CASCADE)

		
class Frase(models.Model):
	frase = models.CharField(max_length=500)
	detalle = models.CharField(max_length=500)
