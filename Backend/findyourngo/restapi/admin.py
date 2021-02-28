from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from findyourngo.restapi.models import NgoAccount, Ngo
from findyourngo.trustworthiness_calculator.TWUpdater import TWUpdater



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

    def save_formset(self, request, form, formset, change):
        try:
            prev_ngo = NgoAccount.objects.get(user_id=formset.instance).ngo

            if not prev_ngo.confirmed:
                prev_ngo.confirmed = True
                prev_ngo.save()
            TWUpdater().update_single_ngo(prev_ngo)
        except:
            print(f'User {formset.instance} previously represented no NGO!')
        instances = formset.save(commit=False)
        for instance in instances:
            instance.save()
            # Warning: This line will call all inlines that use NgoAccount
            if isinstance(instance, NgoAccount):
                TWUpdater().update_single_ngo(instance.ngo)
        formset.save_m2m()


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
