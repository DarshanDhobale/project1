# Generated by Django 4.2.2 on 2023-06-29 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('judge', '0002_userprofile_total_questions'),
    ]

    operations = [
        migrations.AddField(
            model_name='problem',
            name='difficulty',
            field=models.CharField(choices=[('Easy', 'Easy'), ('Medium', 'Medium'), ('Hard', 'Hard')], max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='submission',
            name='language',
            field=models.CharField(choices=[('C++', 'C++'), ('Python', 'Python'), ('Java', 'Java')], default='C++', max_length=10),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='total_score',
            field=models.IntegerField(default=0),
        ),
    ]
