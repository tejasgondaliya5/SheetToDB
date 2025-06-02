from rest_framework import serializers
from .models import Company, Employee
from django.db import connection
import pandas as pd
from django.db import transaction, DatabaseError

class EmployeeBulkUploadSerializer(serializers.Serializer):
    file = serializers.FileField()

    def create(self, validated_data):
        file = validated_data['file']
        try:
            if file.name.endswith('.csv'):
                df = pd.read_csv(file)
            else:
                df = pd.read_excel(file)
        except Exception as e:
            raise serializers.ValidationError({'file': f'Could not read file: {str(e)}'})

        required_columns = [
            'EMPLOYEE_ID', 'FIRST_NAME', 'LAST_NAME', 'PHONE_NUMBER',
            'COMPANY_NAME', 'SALARY', 'MANAGER_ID', 'DEPARTMENT_ID'
        ]
        missing_cols = [col for col in required_columns if col not in df.columns]
        if missing_cols:
            raise serializers.ValidationError({'file': f'Missing columns: {", ".join(missing_cols)}'})

        try:
            with transaction.atomic():
                company_names = df['COMPANY_NAME'].unique()
                existing_companies = Company.objects.filter(name__in=company_names)
                existing_names = set(existing_companies.values_list('name', flat=True))
                new_companies = [Company(name=name) for name in company_names if name not in existing_names]
                Company.objects.bulk_create(new_companies, ignore_conflicts=True)
                companies = {c.name: c for c in Company.objects.filter(name__in=company_names)}

                employees = []
                for row in df.itertuples(index=False):
                    try:
                        employees.append(Employee(
                            employee_id=row.EMPLOYEE_ID,
                            first_name=row.FIRST_NAME,
                            last_name=row.LAST_NAME,
                            phone_number=getattr(row, 'PHONE_NUMBER', None),
                            company=companies[row.COMPANY_NAME],
                            salary=row.SALARY,
                            manager_id=row.MANAGER_ID,
                            department_id=row.DEPARTMENT_ID,
                        ))
                    except Exception as row_err:
                        raise serializers.ValidationError({'row_error': f'Error in row {row}: {str(row_err)}'})

                Employee.objects.bulk_create(employees, ignore_conflicts=True)
                num_queries = len(connection.queries)
        except DatabaseError as db_err:
            raise serializers.ValidationError({'database': f'Database error: {str(db_err)}'})
        except Exception as exc:
            raise serializers.ValidationError({'error': f'Unexpected error: {str(exc)}'})

        return {'message': 'Bulk upload successful.', 'queries_executed': num_queries}
