# Generated by Django 4.2.2 on 2023-07-04 05:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('judge', '0010_alter_testcase_expected_output_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submission',
            name='submitted_at',
            field=models.DateTimeField(),
        ),
    ]