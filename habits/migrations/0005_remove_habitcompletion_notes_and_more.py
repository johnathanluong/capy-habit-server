# Generated by Django 5.1.4 on 2025-01-17 22:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('habits', '0004_alter_habit_modified'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='habitcompletion',
            name='notes',
        ),
        migrations.AlterField(
            model_name='habitcompletion',
            name='status',
            field=models.CharField(choices=[('completed', 'Completed'), ('missed', 'Missed')], default='completed', max_length=10),
        ),
    ]
