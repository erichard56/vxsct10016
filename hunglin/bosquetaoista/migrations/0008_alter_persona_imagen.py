# Generated by Django 5.0.6 on 2024-06-10 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bosquetaoista', '0007_persona_imagen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='persona',
            name='imagen',
            field=models.BinaryField(blank=True, editable=True, null=True),
        ),
    ]
