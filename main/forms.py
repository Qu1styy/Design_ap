import re
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import DesignRequest, Category

class RegisterForm(UserCreationForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    patronymic = forms.CharField(required=False)
    email = forms.EmailField()
    agree = forms.BooleanField()

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'patronymic',
            'username',
            'email',
            'password1',
            'password2',
            'agree'
        )

    def clean_first_name(self):
        if not re.match(r'^[А-Яа-яЁё\- ]+$', self.cleaned_data['first_name']):
            raise forms.ValidationError("Неверный формат имени")
        return self.cleaned_data['first_name']

    def clean_last_name(self):
        if not re.match(r'^[А-Яа-яЁё\- ]+$', self.cleaned_data['last_name']):
            raise forms.ValidationError("Неверный формат фамилии")
        return self.cleaned_data['last_name']

    def clean_username(self):
        if not re.match(r'^[a-zA-Z0-9\-]+$', self.cleaned_data['username']):
            raise forms.ValidationError("Логин только латиница и дефис")
        return self.cleaned_data['username']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()
            user.profile.patronymic = self.cleaned_data['patronymic']
            user.profile.save()

        return user

class DesignRequestForm(forms.ModelForm):
    class Meta:
        model = DesignRequest
        fields = ['title', 'description', 'category', 'photo']

    def clean_photo(self):
        photo = self.cleaned_data.get('photo')

        if not photo:
            raise forms.ValidationError('Фото обязательно')

        return photo

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

from django import forms
from .models import DesignRequest

class AdminStatusForm(forms.ModelForm):
    class Meta:
        model = DesignRequest
        fields = ['status', 'admin_comment', 'result_image']

    def clean_status(self):
        status = self.cleaned_data.get('status')

        if not self.instance or not self.instance.pk:
            return status

        current_status = self.instance.status
        if status == current_status:
            return status

        if current_status == DesignRequest.Status.NEW:
            if status != DesignRequest.Status.IN_PROGRESS:
                raise forms.ValidationError(
                    'Статус "Новая" можно изменить только на "В работе".'
                )
        elif current_status == DesignRequest.Status.IN_PROGRESS:
            if status != DesignRequest.Status.DONE:
                raise forms.ValidationError(
                    'Статус "В работе" можно изменить только на "Выполнено".'
                )
        elif current_status == DesignRequest.Status.DONE:
            raise forms.ValidationError(
                'Статус "Выполнено" менять нельзя.'
            )

        return status

    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get('status')
        comment = cleaned_data.get('admin_comment')
        image = cleaned_data.get('result_image')

        if status == 'done':
            if not comment:
                raise forms.ValidationError(
                    'При выполнении необходимо оставить комментарий'
                )
            if not image:
                raise forms.ValidationError(
                    'При выполнении необходимо загрузить фото'
                )

        return cleaned_data
