from rest_framework.routers import DefaultRouter
from .viewsets import InstitutionViewSet, UserViewSet

router = DefaultRouter()
router.register(r'institutions', InstitutionViewSet)
router.register(r'users', UserViewSet)

urlpatterns = router.urls