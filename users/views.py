from rest_framework import status
from rest_framework.views import APIView
from rest_framework import response
from .serializers import CustomUserSerializer

class UserRegistration(APIView):
    def post(self, request, *args, **kwargs):
        serializer = CustomUserSerializer(data = request.data)
        
        if serializer.is_valid():
            serializer.save()
            return response(serializer.data, status=status.HTTP_201_CREATED)
        
        return response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
