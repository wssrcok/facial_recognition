# Generated by Django 2.1.1 on 2019-02-11 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0003_auto_20190211_0730'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uploadmodel',
            name='upload',
            field=models.ImageField(upload_to='website/static/images'),
        ),
    ]
