# Generated by Django 3.1.3 on 2022-12-22 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gameuser', '0004_auto_20221222_1231'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='gamestatus',
        ),
        migrations.AddField(
            model_name='game',
            name='tictactoe',
            field=models.CharField(default='---------', max_length=9),
        ),
        migrations.DeleteModel(
            name='Gamestate',
        ),
    ]
