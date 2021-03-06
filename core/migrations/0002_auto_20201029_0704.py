# Generated by Django 3.1.1 on 2020-10-29 10:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='team_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.team'),
        ),
        migrations.AlterField(
            model_name='team',
            name='challenge_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.challenge'),
        ),
        migrations.AlterField(
            model_name='team',
            name='judger_assign',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.judge'),
        ),
    ]
