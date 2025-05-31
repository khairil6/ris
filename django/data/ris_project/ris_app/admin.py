# data/ris_app/admin.py

from django.contrib import admin
from .models import Patient, Order, Study, Series, Instance, Report, AuditLog


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ("patient_id", "name", "dob")
    search_fields = ("patient_id", "name")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("accession", "procedure_code", "status")
    list_filter = ("status",)
    search_fields = ("accession", "procedure_code")


@admin.register(Study)
class StudyAdmin(admin.ModelAdmin):
    list_display = ("study_instance_uid", "patient")
    search_fields = ("study_instance_uid", "patient__patient_id", "patient__name")


@admin.register(Series)
class SeriesAdmin(admin.ModelAdmin):
    list_display = ("series_instance_uid", "study")
    search_fields = ("series_instance_uid", "study__study_instance_uid")


@admin.register(Instance)
class InstanceAdmin(admin.ModelAdmin):
    list_display = ("sop_instance_uid", "series")
    search_fields = ("sop_instance_uid", "series__series_instance_uid")


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ("study", "status")
    search_fields = ("study__study_instance_uid", "status")


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ("timestamp", "user", "action", "study")
    list_filter = ("action", "user")
    search_fields = ("user__username", "action", "study__study_instance_uid")
    date_hierarchy = "timestamp"
