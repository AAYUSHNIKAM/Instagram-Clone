# Generated by Django 5.1.6 on 2025-02-18 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0007_postimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, default='default_post.jpg', null=True, upload_to='posts/'),
        ),
    ]
