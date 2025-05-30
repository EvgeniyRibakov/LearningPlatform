# Generated by Django 5.0.6 on 2025-05-26 10:51

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('courses', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='section',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sections', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='test',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_tests', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='test',
            name='section',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tests', to='courses.section'),
        ),
        migrations.AddField(
            model_name='testresult',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='test_results', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='testresult',
            name='test',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='results', to='courses.test'),
        ),
    ]
