# Generated by Django 5.0.6 on 2024-06-10 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bosquetaoista', '0009_alter_persona_imagen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='persona',
            name='imagen',
            field=models.BinaryField(blank=True, editable=True, null=True),
        ),
    ]
