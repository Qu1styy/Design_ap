
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_category_designrequest'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Категорию', 'verbose_name_plural': 'Категории'},
        ),
        migrations.AlterModelOptions(
            name='profile',
            options={'verbose_name': 'Профиль', 'verbose_name_plural': 'Профиля'},
        ),
        migrations.RemoveField(
            model_name='designrequest',
            name='design_image',
        ),
        migrations.AddField(
            model_name='designrequest',
            name='result_image',
            field=models.ImageField(blank=True, null=True, upload_to='design_requests/results/', verbose_name='Фото выполненной работы'),
        ),
    ]
