from django.db import models

class Speciality(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} ({self.code})"

class FullName(models.Model):
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.last_name} {self.middle_name} {self.first_name}".strip()

class Address(models.Model):
    street = models.CharField(max_length=255)
    ward = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    city = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.street}, {self.ward}, {self.district}, {self.city}"

class Doctor(models.Model):
    fullname = models.OneToOneField(FullName, on_delete=models.CASCADE)
    address = models.OneToOneField(Address, on_delete=models.CASCADE)
    speciality = models.ForeignKey(Speciality, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self):
        return str(self.fullname)
