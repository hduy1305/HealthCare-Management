from rest_framework import serializers
from .models import Doctor, FullName, Address, Speciality

class FullNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = FullName
        fields = ('first_name', 'middle_name', 'last_name')

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ('street', 'ward', 'district', 'city')

class SpecialitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Speciality
        fields = ('code', 'name', 'description')

class DoctorSerializer(serializers.ModelSerializer):
    full_name_detail = FullNameSerializer(source='fullname', read_only=True)
    address_detail = AddressSerializer(source='address', read_only=True)
    speciality_detail = SpecialitySerializer(source='speciality', read_only=True)
    full_name_str = serializers.SerializerMethodField()

    class Meta:
        model = Doctor
        fields = (
            'id',
            'full_name_str',
            'full_name_detail',
            'address_detail',
            'speciality_detail',
            'phone_number',
            'email',
        )

    def get_full_name_str(self, obj):
        return str(obj.fullname)