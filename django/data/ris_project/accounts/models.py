from django.db import models
from django.contrib.auth.models import AbstractUser

class Institution(models.Model):
    """
    Maps to HL7 “Sending Facility” (MSH-4) and DICOM MWL Issuer of Accession Number (0040,0022).
    """
    name = models.CharField(max_length=200)
    hl7_facility_code = models.CharField(
        max_length=20,
        help_text="HL7 v2.X facility ID (MSH-4) per HL7 v2 SIU standard"
    )  # HL7 SIU: Scheduled Facility ID :contentReference[oaicite:1]{index=1}
    dicom_station_name = models.CharField(
        max_length=16,
        help_text="DICOM Station Name (0008,1010) for audit/event logs"
    )  # DICOM PS3.6 Tag 0008,1010 :contentReference[oaicite:3]{index=3}

    def __str__(self):
        return f"{self.name} ({self.hl7_facility_code})"


class User(AbstractUser):
    """
    Extends Django’s User to include:
     - institution: which clinic/facility they belong to
     - role: maps to HL7 actor codes (ORM/ORU “actors”) 
     - dicom_ae_title: AE Title used for WADO/STOW calls (IHE SWF)  
    """
    institution = models.ForeignKey(
        Institution, on_delete=models.PROTECT,
        related_name="users",
        null=True,      # ← allow NULL
        blank=True,     # ← allow empty in forms
    )
    ROLE_CHOICES = [
        ('CLINIC_USER',      'Clinic User'),
        ('CLINIC_ADMIN',     'Clinic Admin'),
        ('RADIOLOGIST',      'Radiologist'),
        ('RAD_ADMIN',        'Radiologist Admin'),
    ]
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        help_text="HL7 actor/HL7 ORC-27 Role of this user"
    )  # HL7 ORC segment, “ordering provider” role codes :contentReference[oaicite:5]{index=5}

    dicom_ae_title = models.CharField(
        max_length=16,
        blank=True,
        null=True,
        help_text="DICOM AE Title for this user when issuing WADO/STOW calls"
    )  # DICOM SCU identity for audit/TLS :contentReference[oaicite:7]{index=7}

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
