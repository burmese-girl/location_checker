# Generated by Django 4.1 on 2022-08-19 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('show_ip', '0003_alter_ipaddress_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ipaddress',
            name='create_date',
            field=models.DateTimeField(verbose_name='Create Date'),
        ),
    ]
