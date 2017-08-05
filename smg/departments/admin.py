from django.contrib import admin
from .models import Department, DepartmentSpecialization


class DepartmentSpecializationAdmin(admin.ModelAdmin):
    pass


class DepartmentAdmin(admin.ModelAdmin):
    pass


admin.site.register(DepartmentSpecialization, DepartmentSpecializationAdmin)
admin.site.register(Department, DepartmentAdmin)
