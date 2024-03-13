# Generated by Django 4.2.7 on 2023-12-03 21:56

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('manage', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tb_bee_canales',
            name='apiKey',
        ),
        migrations.AddField(
            model_name='tb_bee_canales',
            name='api_key',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
        migrations.AlterField(
            model_name='tb_bee_canales',
            name='descripcion',
            field=models.TextField(),
        ),
    ]