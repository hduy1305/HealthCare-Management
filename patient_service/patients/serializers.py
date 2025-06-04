# serializers.py
from rest_framework import serializers
from .models import (
    FullName, Address, Patient,
    Outpatient, Inpatient, Emergency,
    MedicalHistory
)

class FullNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = FullName
        fields = ('first_name', 'middle_name', 'last_name')

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ('street', 'district', 'city', 'province')

class MedicalHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalHistory
        fields = ('visit_date', 'diagnosis', 'treatment')

class BasePatientSerializer(serializers.ModelSerializer):
    full_name_detail = FullNameSerializer(source='fullname', read_only=True)
    address_detail = AddressSerializer(source='address', read_only=True)
    full_name_str = serializers.SerializerMethodField()
    patient_type = serializers.SerializerMethodField()

    class Meta:
        model = Patient
        fields = (
            'id',
            'full_name_str',
            'full_name_detail',
            'address_detail',
            'phone',
            'email',
            'date_of_birth',
            'gender',
            'created_at',
            'patient_type',
        )

    def get_full_name_str(self, obj):
        return str(obj.fullname)

    def get_patient_type(self, obj):
        return obj.get_patient_type()

class OutpatientSerializer(BasePatientSerializer):
    visit_reason = serializers.CharField(source='outpatient.visit_reason', read_only=True)

    class Meta(BasePatientSerializer.Meta):
        model = Outpatient
        fields = BasePatientSerializer.Meta.fields + ('visit_reason',)

class InpatientSerializer(BasePatientSerializer):
    room_number = serializers.CharField(source='inpatient.room_number', read_only=True)
    admission_date = serializers.DateField(source='inpatient.admission_date', read_only=True)
    discharge_date = serializers.DateField(source='inpatient.discharge_date', read_only=True)

    class Meta(BasePatientSerializer.Meta):
        model = Inpatient
        fields = BasePatientSerializer.Meta.fields + (
            'room_number', 'admission_date', 'discharge_date'
        )

class EmergencySerializer(BasePatientSerializer):
    emergency_level = serializers.CharField(source='emergency.emergency_level', read_only=True)
    arrival_time = serializers.DateTimeField(source='emergency.arrival_time', read_only=True)
    notes = serializers.CharField(source='emergency.notes', read_only=True)

    class Meta(BasePatientSerializer.Meta):
        model = Emergency
        fields = BasePatientSerializer.Meta.fields + (
            'emergency_level', 'arrival_time', 'notes'
        )

# You can choose to register different ViewSets/Views for each subtype
# or use a single PatientSerializer for general listing.