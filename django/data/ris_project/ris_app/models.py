# ris_app/models.py
from django.conf import settings
from django.db import models
from django.db.models import JSONField  # use JSONField for PostgreSQL; for SQLite use TextField

class Patient(models.Model):
    patient_id = models.CharField(max_length=64, unique=True)   # DICOM (0010,0020) Patient ID :contentReference[oaicite:0]{index=0}
    name       = models.CharField(max_length=200)               # DICOM (0010,0010) Patient Name :contentReference[oaicite:1]{index=1}
    dob        = models.DateField()                             # DICOM (0010,0030) Patient Birth Date :contentReference[oaicite:2]{index=2}

class Order(models.Model):
    accession      = models.CharField(max_length=64, unique=True)  # HL7 ORM: Placer/Accession Number :contentReference[oaicite:3]{index=3}
    procedure_code = models.CharField(max_length=64)               # HL7 ORU: Procedure Code Identifier :contentReference[oaicite:4]{index=4}
    status         = models.CharField(max_length=32)               # e.g. “SCHEDULED”, “COMPLETED” :contentReference[oaicite:5]{index=5}

class Study(models.Model):
    study_instance_uid = models.CharField(max_length=64, unique=True)  # DICOM (0020,000D) Study Instance UID :contentReference[oaicite:6]{index=6}
    patient            = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='studies')

class Series(models.Model):
    series_instance_uid = models.CharField(max_length=64, unique=True)  # DICOM (0020,000E) Series Instance UID :contentReference[oaicite:7]{index=7}
    study                = models.ForeignKey(Study, on_delete=models.CASCADE, related_name='series')

class Instance(models.Model):
    sop_instance_uid = models.CharField(max_length=64, unique=True)  # DICOM (0008,0018) SOP Instance UID :contentReference[oaicite:8]{index=8}
    series           = models.ForeignKey(Series, on_delete=models.CASCADE, related_name='instances')

class Report(models.Model):
    study       = models.OneToOneField(Study, on_delete=models.CASCADE, related_name='report')
    status      = models.CharField(max_length=32)     # e.g. “FINAL”, “PRELIM”
    content     = models.TextField()                  # free-text report
    fhir_payload= JSONField()                         # full FHIR DiagnosticReport :contentReference[oaicite:9]{index=9}

class AuditLog(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)                
    user      = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    action    = models.CharField(max_length=64)         # e.g. “CREATE_ORDER”, “VIEW_STUDY”
    study     = models.ForeignKey(Study, on_delete=models.CASCADE)
