from rest_framework import viewsets, status
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from django.db.models import Q
from app.item.models import ItemList
from app.item.serializers import ItemListSerializer

from .models import Event, AudioNote, EventImage
from .serializers import EventSerializer, EventImageSerializer, AudioNoteSerializer

class EventViewSet(viewsets.ModelViewSet): 

    queryset = Event.objects.all()
    serializer_class = EventImageSerializer 
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_permissions(self): 
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated()]
        return [AllowAny()]

    def get_queryset(self): 
        # sobreescribimos el método para mostrar los eventos organizados o en los que participa el cliente.
        user = self.request.user 
        if user.is_authenticated: 
            events = Event.objects.filter(Q(organizer=user) | Q(participants=user)).distinct()
            return events 

        raise PermissionDenied("Usuario no autenticado. Por favor, incluye un token de acceso")

    @action(detail=True, methods=['POST'], permission_classes=[IsAuthenticated])
    def add_image(self, request, pk=None):
        # Personalizamos la acción para añadir imágenes a un evento 
        event = self.get_object()
        serializer = EventImageSerializer(data=request.data) 

        if serializer.is_valid(): 
            serializer.save(event=event) # Guardamos la imágen asociada al evento 
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['POST'], permission_classes=[IsAuthenticated])
    def add_note_audio(self, request, pk=None): 
        event = self.get_object()
        serializer = AudioNoteSerializer(data=request.data)

        if serializer.is_valid(): 
            serializer.save(event=event)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['GET'], permission_classes=[IsAuthenticated])
    def item_list(self, request, pk=None): 
        event = self.get_object()
        item_list, created = ItemList.objects.get_or_create(event=event)
        serializer = ItemListSerializer(item_list)
        return Response(serializer.data)

