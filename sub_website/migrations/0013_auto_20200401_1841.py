# Generated by Django 3.0.4 on 2020-04-01 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sub_website', '0012_product_last_cat'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='last_cat',
            field=models.CharField(max_length=256),
        ),
    ]
