# Generated by Django 3.1.2 on 2020-10-26 02:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('process_order', '0002_auto_20201025_1746'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='order',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='products', to='process_order.order'),
        ),
    ]
