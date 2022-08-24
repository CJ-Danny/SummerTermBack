# Generated by Django 4.0.6 on 2022-08-08 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EmailCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=30)),
                ('code', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('ID', models.IntegerField(primary_key=True, serialize=False)),
                ('nickname', models.CharField(max_length=20)),
                ('password', models.CharField(max_length=20)),
                ('email', models.CharField(max_length=30, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('userID', models.IntegerField(primary_key=True, serialize=False)),
                ('selfAvatar', models.IntegerField()),
                ('avatar', models.FileField(default='publicAvatar/public0.jpg', upload_to='avatars/')),
                ('description', models.CharField(max_length=150)),
                ('realname', models.CharField(max_length=20)),
            ],
        ),
    ]
