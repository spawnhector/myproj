# Generated by Django 4.0.8 on 2023-01-24 17:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('schannels', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscriber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('channel_type', models.CharField(max_length=150)),
                ('channel', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='_subscriber', to='schannels.schannel')),
            ],
        ),
    ]
