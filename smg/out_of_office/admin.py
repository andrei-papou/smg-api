from django.contrib import admin
from .models import TimeShift, Vacation, BusinessLeave, Unpaid


common_fields = ['id', 'start', 'end', 'employee']


class OOOAdmin(admin.ModelAdmin):
    list_display = common_fields


admin.site.register(TimeShift, OOOAdmin)
admin.site.register(Vacation, OOOAdmin)
admin.site.register(BusinessLeave, OOOAdmin)
admin.site.register(Unpaid, OOOAdmin)
