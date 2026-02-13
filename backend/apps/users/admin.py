from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, UserProfile, UserSession


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profil'
    fk_name = 'user'


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Administration des utilisateurs uFaranga."""

    inlines = [UserProfileInline]

    list_display = [
        'email', 'first_name', 'last_name', 'phone_number',
        'kyc_level', 'is_phone_verified', 'is_email_verified',
        'is_active', 'created_at',
    ]
    list_filter = [
        'is_active', 'is_staff', 'kyc_level',
        'is_phone_verified', 'is_email_verified',
        'country', 'created_at',
    ]
    search_fields = ['email', 'first_name', 'last_name', 'phone_number']
    ordering = ['-created_at']
    readonly_fields = ['id', 'created_at', 'updated_at', 'last_login_ip']

    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Informations personnelles', {
            'fields': ('first_name', 'last_name', 'phone_number', 'date_of_birth')
        }),
        ('Adresse', {
            'fields': ('country', 'city', 'address')
        }),
        ('Vérifications', {
            'fields': ('is_phone_verified', 'is_email_verified', 'kyc_level')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Métadonnées', {
            'fields': ('id', 'created_at', 'updated_at', 'last_login_ip', 'last_login'),
            'classes': ('collapse',),
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'username', 'first_name', 'last_name',
                'phone_number', 'password1', 'password2',
            ),
        }),
    )


@admin.register(UserSession)
class UserSessionAdmin(admin.ModelAdmin):
    """Administration des sessions utilisateur."""

    list_display = ['user', 'ip_address', 'is_active', 'created_at', 'last_activity']
    list_filter = ['is_active', 'created_at']
    search_fields = ['user__email', 'ip_address']
    ordering = ['-last_activity']
    readonly_fields = ['user', 'session_key', 'ip_address', 'user_agent', 'device_info', 'created_at']
