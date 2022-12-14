# Generated by Django 4.0.6 on 2022-08-08 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('ID', models.AutoField(primary_key=True, serialize=False)),
                ('groupName', models.CharField(max_length=20, unique=True)),
                ('ownerID', models.IntegerField()),
                ('createTime', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='UserGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userID', models.IntegerField()),
                ('groupID', models.IntegerField()),
                ('position', models.IntegerField()),
            ],
        ),
    ]
