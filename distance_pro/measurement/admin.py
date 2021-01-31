from django.contrib import admin
from .models import Measurement
# Register your models here.
@admin.register(Measurement)
class MeasurementAdminmodel(admin.ModelAdmin):
     list_display = ('id','location','destination','distance','created')