# Generated by Django 4.2 on 2024-11-25 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ContactUs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300, verbose_name='عنوان')),
                ('email', models.EmailField(max_length=300, verbose_name='ایمیل')),
                ('full_name', models.CharField(max_length=300, verbose_name='نام و نام خانوادگی')),
                ('message', models.TextField(verbose_name='پیام')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='ایجاد شده در')),
                ('response', models.TextField(blank=True, null=True, verbose_name='پاسخ')),
                ('is_read_by_admin', models.BooleanField(default=False, verbose_name=' خوانده شده توسط مدیر ')),
            ],
            options={
                'verbose_name': 'تماس',
                'verbose_name_plural': 'تماس ها',
            },
        ),
        migrations.CreateModel(
            name='ProfileModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images', verbose_name='تصویر پروفایل')),
            ],
        ),
    ]
