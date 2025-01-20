# Generated by Django 5.1.4 on 2025-01-19 23:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gacha_items', '0002_alter_accessory_rarity'),
        ('habits', '0008_alter_habit_accessory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='habit',
            name='accessory',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='habits', to='gacha_items.accessory'),
        ),
    ]
