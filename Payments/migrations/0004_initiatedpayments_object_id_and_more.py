# Generated by Django 4.2.3 on 2024-01-18 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Payments', '0003_projectpayments'),
    ]

    operations = [
        migrations.AddField(
            model_name='initiatedpayments',
            name='object_id',
            field=models.CharField(default='1', max_length=30),
        ),
        migrations.AddField(
            model_name='initiatedpayments',
            name='purpose',
            field=models.CharField(default='Charity', max_length=30),
        ),
    ]
