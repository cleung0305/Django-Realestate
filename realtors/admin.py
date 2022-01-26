from django.contrib import admin

from .models import Realtor

class RealtorAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'phone', 'email', 'hire_date', 'is_mvp']
    list_display_links = ['id', 'name']
    search_fields = ['f_name', 'l_name',]
    list_per_page = 25

    def name(self, obj):
        return f'{obj.f_name} {obj.l_name}'

admin.site.register(Realtor, RealtorAdmin)