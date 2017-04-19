from django.contrib import admin
from monitor.models import Report, Item, Case

# Register your models here.

admin.site.register(Report)
admin.site.register(Item)
admin.site.register(Case)