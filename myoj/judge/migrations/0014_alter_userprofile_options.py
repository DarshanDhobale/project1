# Generated by Django 4.2.2 on 2023-09-06 11:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('judge', '0013_alter_testcase_problem'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userprofile',
            options={'ordering': ['-total_score']},
        ),
    ]
