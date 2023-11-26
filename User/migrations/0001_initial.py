# Generated by Django 4.2.1 on 2023-10-24 14:16

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.CharField(default=uuid.uuid4, max_length=36, primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=200)),
                ('role', models.CharField(default='NORMAL', max_length=100)),
                ('birthday', models.CharField(max_length=200)),
                ('gender', models.CharField(choices=[('MALE', 'MALE'), ('FEMALE', 'FEMALE')], max_length=10)),
                ('createdAt', models.DateField(auto_now_add=True)),
                ('updateAt', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='AccountProfile',
            fields=[
                ('userID', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='User.account')),
                ('userAvt', models.URLField(blank=True, null=True)),
                ('userBackGround', models.URLField(blank=True, null=True)),
            ],
        ),
    ]
