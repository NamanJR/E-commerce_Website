# Generated by Django 4.0.4 on 2022-05-18 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='no',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='sku_id',
            field=models.CharField(default=0, max_length=100, null=True),
        ),
    ]
