# Generated by Django 4.2.2 on 2023-07-02 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('judge', '0006_problem_time_limit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='problem',
            name='difficulty',
            field=models.CharField(choices=[('l1', 'Easy'), ('l2', 'Medium'), ('l3', 'Hard')], max_length=10, null=True),
        ),
    ]
