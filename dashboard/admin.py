from django.contrib import admin
from .models import Contributions, LoansRequest
from django.contrib.auth.models import Group

# Changing the default Django Title on admin page
admin.site.site_header = 'TheGentleMens Club Dashboard'

# TO REARRANGE THE DISPLAY OF TABLES
class ContributionsAdmin(admin.ModelAdmin):
    list_display = ('name','amount','month')
    list_filter = ('month',)
# Register your models here.
admin.site.register(Contributions,ContributionsAdmin)
admin.site.register(LoansRequest)
# admin.site.unregister(Group)
