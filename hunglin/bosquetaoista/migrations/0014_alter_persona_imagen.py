# Generated by Django 5.0.6 on 2024-06-10 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bosquetaoista', '0013_alter_persona_imagen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='persona',
            name='imagen',
            field=models.ImageField(blank=True, null=True, upload_to='images/', verbose_name=''),
        ),
    ]
