# Generated by Django 5.1.1 on 2024-10-13 02:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('canchas', '0007_ownerestablecimiento_fecha_nacimiento'),
    ]

    operations = [
        migrations.AddField(
            model_name='reserva',
            name='codigo_operacion',
            field=models.CharField(max_length=20, null=True, verbose_name='Código operación'),
        ),
    ]
