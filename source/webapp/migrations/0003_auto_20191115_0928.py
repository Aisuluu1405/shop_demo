# Generated by Django 2.1 on 2019-11-15 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0002_auto_20191107_1442'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='in_order',
            field=models.BooleanField(default=True, verbose_name='В наличии'),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('new', 'Новый'), ('payed', 'Оплачен'), ('processing', 'Обработка'), ('delivered', 'Доставлен'), ('canceled', 'Отменён')], default='new', max_length=20, verbose_name='Статус'),
        ),
    ]
