# Generated by Django 4.0.8 on 2023-01-24 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('subscriber', '0001_initial'),
        ('schannels', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='schannel',
            name='subscribers',
            field=models.ManyToManyField(blank=True, to='subscriber.subscriber'),
        ),
    ]
