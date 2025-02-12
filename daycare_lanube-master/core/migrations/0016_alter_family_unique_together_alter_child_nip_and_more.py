# Generated by Django 5.0.2 on 2024-09-04 00:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_alter_bill_month_alter_bill_paid_alter_child_nip_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='family',
            unique_together=set(),
        ),
        migrations.AlterField(
            model_name='child',
            name='nip',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterUniqueTogether(
            name='child',
            unique_together={('nip', 'active')},
        ),
    ]
