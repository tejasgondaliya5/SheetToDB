from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import EmployeeBulkUploadSerializer
from django.db import reset_queries

class EmployeeBulkUploadView(APIView):
    def post(self, request):
        reset_queries()
        serializer = EmployeeBulkUploadSerializer(data=request.data)
        if serializer.is_valid():
            result = serializer.save()
            return Response(result, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)