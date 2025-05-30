# data/ris_app/urls.py
from rest_framework.routers import DefaultRouter
from .viewsets import (
    PatientViewSet, 
    OrderViewSet,
    StudyViewSet, 
    SeriesViewSet,
    InstanceViewSet, 
    ReportViewSet,
    AuditLogViewSet,
)

router = DefaultRouter()
router.register(r'patients', PatientViewSet, basename='patient')
router.register(r'orders',   OrderViewSet,   basename='order')
router.register(r'studies',  StudyViewSet,   basename='study')
router.register(r'series',   SeriesViewSet,  basename='series')
router.register(r'instances',InstanceViewSet,basename='instance')
router.register(r'reports',  ReportViewSet,  basename='report')
router.register(r'audit',    AuditLogViewSet,basename='audit')

urlpatterns = router.urls
