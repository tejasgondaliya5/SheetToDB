from django.contrib import admin
from .models import Company, Employee

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = (
        'employee_id', 'first_name', 'last_name', 'phone_number',
        'company', 'salary', 'manager_id', 'department_id'
    )
    search_fields = ('first_name', 'last_name', 'employee_id', 'company__name')
    list_filter = ('company', 'department_id', 'manager_id')