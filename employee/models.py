from django.db import models

class Company(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Employee(models.Model):
    employee_id = models.IntegerField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15, null=True, blank=True)  # Now nullable
    company = models.ForeignKey(Company, related_name='employees', on_delete=models.CASCADE)
    salary = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)  # Now nullable
    manager_id = models.IntegerField(null=True, blank=True)  # Now nullable
    department_id = models.IntegerField(null=True, blank=True)  # Now nullable

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
