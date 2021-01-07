from django.contrib import admin
from .models import Hospital, Company, Sick, Employee, DeliveryReport

# Register your models here.
admin.site.register(Hospital)
admin.site.register(Company)
admin.site.register(Sick)
admin.site.register(Employee)
admin.site.register(DeliveryReport)
