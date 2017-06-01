from django.contrib import admin
from monitor.models import Report, Item, Case, Item_Error

# Register your models here.

admin.site.register(Report)
admin.site.register(Item)
admin.site.register(Item_Error)
admin.site.register(Case)
