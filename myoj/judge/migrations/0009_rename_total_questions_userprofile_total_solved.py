# Generated by Django 4.2.2 on 2023-07-03 10:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('judge', '0008_alter_problem_difficulty'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='total_questions',
            new_name='total_solved',
        ),
    ]
