from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.models import Group

from .models import User


class UserCreationFormExtended(UserCreationForm):

    class Meta:
        model = User
        fields = '__all__'


class UserChangeFormExtended(UserChangeForm):

    class Meta:
        model = User
        fields = '__all__'


class UserAdminCustom(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name',
                    'is_superuser', 'is_admin', 'is_moderator', 'role',
                    'confirmation_code', )
    list_filter = ('is_staff', 'is_superuser')
    search_fields = ('username', )
    form = UserChangeFormExtended
    add_form = UserCreationFormExtended

    fieldsets = (
        (None, {'fields': ('username', 'password', 'role')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email',
                                      'bio')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'role')}
         ),
    )


admin.site.register(User, UserAdminCustom)
admin.site.unregister(Group)
