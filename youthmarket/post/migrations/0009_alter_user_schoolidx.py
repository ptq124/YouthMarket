# Generated by Django 3.2.13 on 2022-07-23 16:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0008_alter_user_schoolidx'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='schoolIdx',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='post.school', verbose_name='학교idx'),
        ),
    ]
