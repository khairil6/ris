from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from .models import Institution, User
from .serializers import InstitutionSerializer, UserSerializer
from .permissions import IsClinicAdmin, IsRadiologist

class InstitutionViewSet(viewsets.ModelViewSet):
    queryset = Institution.objects.all()
    serializer_class = InstitutionSerializer
    permission_classes = [IsAuthenticated, IsClinicAdmin]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'hl7_facility_code']

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.select_related('institution').all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsClinicAdmin]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['username', 'email', 'role']