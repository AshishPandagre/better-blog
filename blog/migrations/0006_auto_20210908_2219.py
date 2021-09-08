# Generated by Django 3.2.5 on 2021-09-08 16:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_rename_reply_comment_parent'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='opinion',
            name='content_type',
        ),
        migrations.RemoveField(
            model_name='opinion',
            name='object_id',
        ),
        migrations.AddField(
            model_name='opinion',
            name='comment',
            field=models.ForeignKey(default=31, on_delete=django.db.models.deletion.CASCADE, to='blog.comment'),
            preserve_default=False,
        ),
    ]
