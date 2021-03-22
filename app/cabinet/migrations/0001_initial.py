# Generated by Django 3.1.3 on 2021-03-22 11:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0002_defaultobject'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cabinet',
            fields=[
                ('defaultobject_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.defaultobject')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Właściciel szafy')),
            ],
            options={
                'verbose_name': 'Cabinet',
                'verbose_name_plural': 'Cabinets',
            },
            bases=('core.defaultobject', models.Model),
        ),
    ]
