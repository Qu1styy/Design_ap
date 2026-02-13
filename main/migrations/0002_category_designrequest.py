
import django.db.models.deletion
import main.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Название категории')),
            ],
        ),
        migrations.CreateModel(
            name='DesignRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Название')),
                ('description', models.TextField(verbose_name='Описание')),
                ('photo', models.ImageField(upload_to='design_requests/photos/', validators=[main.models.validate_image_size, main.models.validate_image_extension], verbose_name='Фото помещения / план')),
                ('design_image', models.ImageField(blank=True, null=True, upload_to='design_requests/designs/', verbose_name='Готовый дизайн')),
                ('admin_comment', models.TextField(blank=True, null=True, verbose_name='Комментарий администратора')),
                ('status', models.CharField(choices=[('new', 'Новая'), ('in_progress', 'Принято в работу'), ('done', 'Выполнено')], default='new', max_length=20, verbose_name='Статус')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.category', verbose_name='Категория')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Заявка на дизайн',
                'verbose_name_plural': 'Заявки на дизайн',
                'ordering': ['-created_at'],
            },
        ),
    ]
