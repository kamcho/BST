# Generated by Django 4.2.3 on 2024-02-14 23:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Charity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateField(auto_now=True)),
                ('closes_on', models.DateField()),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(max_length=3000)),
                ('target', models.PositiveIntegerField()),
                ('totals', models.PositiveIntegerField()),
                ('archived', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='ChurchProjects',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateField(auto_now=True)),
                ('closes_on', models.DateField()),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(max_length=3000)),
                ('target', models.PositiveIntegerField()),
                ('archived', models.BooleanField(default=False)),
                ('completed', models.BooleanField(default=False)),
            ],
        ),
    ]
