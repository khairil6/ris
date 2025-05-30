# ris_app/services/orthanc.py
import requests
from django.conf import settings

class OrthancClient:
    def __init__(self):
        self.base = settings.ORTHANC_URL             # e.g. https://nas.example.com:8042
        self.auth = (settings.ORTHANC_USER, settings.ORTHANC_PASS)

    def qido_studies(self, params=None):
        """Query worklist via QIDO-RS (DICOMweb) :contentReference[oaicite:10]{index=10}"""
        r = requests.get(f"{self.base}/qido/studies", auth=self.auth, params=params)
        r.raise_for_status()
        return r.json()

    def wado_instance(self, study_uid, series_uid, instance_uid):
        """Fetch pixel data via WADO-RS :contentReference[oaicite:11]{index=11}"""
        url = f"{self.base}/wado/{study_uid}/{series_uid}/{instance_uid}"
        r = requests.get(url, auth=self.auth)
        r.raise_for_status()
        return r.content

    def stow_instances(self, dicom_files: list):
        """Send new objects via STOW-RS :contentReference[oaicite:12]{index=12}"""
        files = [('file', ('instance.dcm', f, 'application/dicom')) for f in dicom_files]
        r = requests.post(f"{self.base}/stow", auth=self.auth, files=files)
        r.raise_for_status()
        return r.json()
