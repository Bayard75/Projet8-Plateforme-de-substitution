# Generated by Django 3.0.4 on 2020-03-30 22:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sub_website', '0003_auto_20200330_2149'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='codebar',
            field=models.CharField(max_length=100, primary_key=True, serialize=False),
        ),
    ]
