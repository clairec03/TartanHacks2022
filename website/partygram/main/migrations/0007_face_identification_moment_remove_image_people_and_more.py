# Generated by Django 4.0.2 on 2022-02-06 03:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_rename_img_image_image_file'),
    ]

    operations = [
        migrations.CreateModel(
            name='Face',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.JSONField()),
                ('landmark', models.JSONField()),
            ],
        ),
        migrations.CreateModel(
            name='Identification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('encoding', models.JSONField()),
            ],
        ),
        migrations.CreateModel(
            name='Moment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('picture', models.ImageField(default=None, upload_to='')),
            ],
        ),
        migrations.RemoveField(
            model_name='image',
            name='people',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='pfp',
        ),
        migrations.AddField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(default=None, upload_to=''),
        ),
        migrations.DeleteModel(
            name='Encoding',
        ),
        migrations.DeleteModel(
            name='Image',
        ),
        migrations.AddField(
            model_name='identification',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.profile'),
        ),
        migrations.AddField(
            model_name='face',
            name='moment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.moment'),
        ),
        migrations.AddField(
            model_name='face',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.profile'),
        ),
    ]