from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    patronymic = models.CharField(
        max_length=150,
        verbose_name='Отчество',
        blank=True
    )

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профиля'

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


def validate_image_size(image):
    if image.size > 2 * 1024 * 1024:
        raise ValidationError('Размер изображения не должен превышать 2 МБ')


def validate_image_extension(value):
    allowed = ['jpg', 'jpeg', 'png', 'bmp']
    ext = value.name.split('.')[-1].lower()
    if ext not in allowed:
        raise ValidationError('Недопустимый формат изображения')


class Category(models.Model):
    name = models.CharField(
        'Название категории',
        max_length=100,
        unique=True
    )

    class Meta:
        verbose_name = 'Категорию'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

class DesignRequest(models.Model):
    class Status(models.TextChoices):
        NEW = 'new', 'Новая'
        IN_PROGRESS = 'in_progress', 'Принято в работу'
        DONE = 'done', 'Выполнено'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )

    title = models.CharField('Название', max_length=200)
    description = models.TextField('Описание')

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name='Категория'
    )

    photo = models.ImageField(
        'Фото помещения / план',
        upload_to='design_requests/photos/',
        validators=[validate_image_size, validate_image_extension]
    )

    result_image = models.ImageField(
        'Фото выполненной работы',
        upload_to='design_requests/results/',
        blank=True,
        null=True
    )

    admin_comment = models.TextField(
        'Комментарий администратора',
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.NEW,
        verbose_name='Статус'
    )

    created_at = models.DateTimeField(
        'Дата создания',
        auto_now_add=True
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Заявка на дизайн'
        verbose_name_plural = 'Заявки на дизайн'

    def __str__(self):
        return self.title
