# Generated by Django 2.1.3 on 2019-03-15 03:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_auto_20190313_1627'),
    ]

    operations = [
        migrations.AddField(
            model_name='survey',
            name='endTime',
            field=models.CharField(default=0, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='survey',
            name='lowTide',
            field=models.CharField(default=0, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='survey',
            name='lowTideTime',
            field=models.CharField(default=0, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='survey',
            name='startTime',
            field=models.CharField(default=0, max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='survey',
            name='clams',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='survey',
            name='location',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='survey',
            name='surveyName',
            field=models.CharField(max_length=200),
        ),
    ]