# Generated by Django 5.0.5 on 2024-05-16 20:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bosquetaoista', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tipos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=20)),
                ('descripcion', models.CharField(max_length=50)),
                ('ident', models.CharField(max_length=10)),
            ],
        ),
    ]
