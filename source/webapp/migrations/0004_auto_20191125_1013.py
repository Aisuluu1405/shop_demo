# Generated by Django 2.1 on 2019-11-25 10:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0003_auto_20191115_0928'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'permissions': [('deliver_order', 'Может доставить заказ')], 'verbose_name': 'Заказ', 'verbose_name_plural': 'Заказы'},
        ),
        migrations.AlterField(
            model_name='order',
            name='email',
            field=models.EmailField(blank=True, max_length=50, null=True, verbose_name='Email'),
        ),
        migrations.AlterField(
            model_name='order',
            name='first_name',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Имя'),
        ),
        migrations.AlterField(
            model_name='order',
            name='last_name',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Фамилия'),
        ),
        migrations.AlterField(
            model_name='orderproduct',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_products', to='webapp.Order', verbose_name='Заказ'),
        ),
        migrations.AlterField(
            model_name='orderproduct',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_products', to='webapp.Product', verbose_name='Товар'),
        ),
    ]
