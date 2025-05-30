from rest_framework import serializers
from .models import Institution, User

class InstitutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institution
        fields = ['id', 'name', 'hl7_facility_code', 'dicom_station_name']

class UserSerializer(serializers.ModelSerializer):
    institution = InstitutionSerializer(read_only=True)
    institution_id = serializers.PrimaryKeyRelatedField(
        queryset=Institution.objects.all(), source='institution', write_only=True
    )

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'institution', 'institution_id', 'role', 'dicom_ae_title'
        ]
        read_only_fields = ['id']