from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from findyourngo.restapi.models import NgoAccount, Ngo


class NgoAccountInline(admin.StackedInline):
    model = NgoAccount
    can_delete = False

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'ngo':
            return CategoryChoiceField(queryset=Ngo.objects.all())
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class CategoryChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return f'{obj.id}: {obj.name}'


# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (NgoAccountInline,)


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
