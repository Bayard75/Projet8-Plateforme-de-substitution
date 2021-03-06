# Generated by Django 3.0.4 on 2020-03-31 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sub_website', '0009_auto_20200331_1513'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('name', models.CharField(max_length=256, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('codebar', models.CharField(max_length=128, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=256)),
                ('grade', models.CharField(max_length=1)),
                ('url', models.URLField()),
                ('reperes', models.URLField()),
                ('image', models.URLField()),
                ('categories', models.ManyToManyField(related_name='products', to='sub_website.Category')),
            ],
        ),
    ]
