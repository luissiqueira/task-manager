# Generated by Django 2.2.7 on 2019-11-12 00:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0003_project_creator'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='creator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Criador'),
        ),
        migrations.AddField(
            model_name='task',
            name='creator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Criador'),
        ),
        migrations.AddField(
            model_name='tasknote',
            name='creator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Criador'),
        ),
        migrations.AlterField(
            model_name='project',
            name='creator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Criador'),
        ),
        migrations.CreateModel(
            name='ObjectRole',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Data de criação')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Data de modificação')),
                ('deleted', models.BooleanField(default=False, verbose_name='Deletado?')),
                ('object_id', models.PositiveIntegerField()),
                ('role', models.CharField(choices=[('admin', 'Administrador'), ('operational', 'Operador'), ('viewer', 'Visualizador')], default='viewer', max_length=80, verbose_name='Papel')),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
                ('creator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Criador')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='roles', to=settings.AUTH_USER_MODEL, verbose_name='Usuário')),
            ],
            options={
                'verbose_name': 'Papel',
                'verbose_name_plural': 'Papéis',
                'ordering': ('created_at',),
            },
        ),
        migrations.CreateModel(
            name='ObjectAttachment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Data de criação')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Data de modificação')),
                ('deleted', models.BooleanField(default=False, verbose_name='Deletado?')),
                ('object_id', models.PositiveIntegerField()),
                ('attachment', models.FileField(upload_to='', verbose_name='Anexo')),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
                ('creator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Criador')),
            ],
            options={
                'verbose_name': 'Papel',
                'verbose_name_plural': 'Papéis',
                'ordering': ('created_at',),
            },
        ),
    ]
