# Generated by Django 2.2.4 on 2022-10-04 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0002_books_uploadby'),
    ]

    operations = [
        migrations.AddField(
            model_name='books',
            name='updated_at',
            field=models.DateField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='books',
            name='created_at',
            field=models.DateField(auto_now_add=True),
        ),
    ]
