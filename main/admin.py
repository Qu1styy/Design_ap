from django.contrib import admin
from django.contrib.auth.models import User
from .models import Profile, DesignRequest, Category


# ===== Категории =====
admin.site.register(Category)



# ===== Inline заявок =====
class DesignRequestInline(admin.StackedInline):
    model = DesignRequest
    extra = 0
    show_change_link = True
    readonly_fields = ('created_at',)


# ===== Профиль пользователя =====
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Дополнительные данные'


# ===== Админка пользователя =====
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'last_name', 'first_name', 'get_patronymic')
    search_fields = ('username', 'last_name', 'first_name')

    inlines = (ProfileInline, DesignRequestInline)

    def get_patronymic(self, obj):
        return obj.profile.patronymic
    get_patronymic.short_description = 'Отчество'


# ===== Перерегистрация User =====
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


# ===== Отдельная админка заявок (на всякий случай) =====
@admin.register(DesignRequest)
class DesignRequestAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'user',
        'category',
        'status',
        'created_at',
    )
    list_filter = ('status', 'category')
    search_fields = ('title', 'description')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)