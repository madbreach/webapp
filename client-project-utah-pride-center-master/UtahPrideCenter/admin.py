from django.contrib import admin

# Register your models here.
from django.utils.html import format_html

from UtahPrideCenter import models


@admin.register(models.Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('user', 'section', 'check_in_time')
    fields = ('user', 'section', 'check_in_time')
    def has_add_permission(self, request, obj=None):
        return False


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'display_name', 'pronouns', 'specified_pronouns')
    fields = ('first_name', 'last_name', 'display_name', 'pronouns', 'specified_pronouns')


@admin.register(models.UserSection)
class UserSectionAdmin(admin.ModelAdmin):
    list_display = ('user', 'section')
    fields = ('user', 'section')


@admin.register(models.JoinLink)
class JoinLinkAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_link', 'link_creation_time')
    fields = ('user', 'full_link', 'link_creation_time')
    readonly_fields = ('full_link', 'link_creation_time')

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('user',)
        return self.readonly_fields

    def full_link(self, obj):
        return format_html(
            '<a href="javascript:navigator.clipboard.writeText(location.origin+\'{url}\')">Copy Link</a>',
            url=obj.full_link)

    full_link.short_description = 'Link'


@admin.register(models.Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    fields = ('name', 'description')

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('name',)
        return self.readonly_fields


@admin.register(models.Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'program')
    fields = ('name', 'program', 'zoom_link')


@admin.register(models.Pronoun)
class PronounAdmin(admin.ModelAdmin):
    fields = ('text', 'user_specified')