from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from .serializer import UserRegistrationSerializer, UserProfileSerializer
from django.contrib.auth.models import User 

class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserProfileSerializer

    # Permisos personalizados
    def get_permissions(self):
        if self.action in ['create', 'register', 'rest_password']:
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_serializer_class(self): 
        # Seleccionamos un serializador según la acción 
        if self.action == 'create': 
            return UserRegistrationSerializer
        return UserProfileSerializer

    @action(detail=False, methods=['POST'], permission_classes=[AllowAny])
    def register(self, request): 

        serializer = UserRegistrationSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            # Obtenemos los datos del perfil para la respuesta 
            profile_serializer = UserProfileSerializer(user)
            return Response(profile_serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def profile(self, request):

        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
