from django.contrib import admin
from .models import FullName, Address, Outpatient, Inpatient, Emergency

# Register your models here.
admin.site.register(FullName)
admin.site.register(Address)
admin.site.register(Outpatient)
admin.site.register(Inpatient)
admin.site.register(Emergency)