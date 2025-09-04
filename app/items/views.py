from rest_framework import viewsets 
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import Item, ItemList 
from .serializers import ItemSerializer

class ItemViewSet(viewsets.ModelViewSet):

    queryset = Item.objects.all()
    serializer_class = ItemSerializer 

    def get_permissions(self): 
        # Personalizamos los permisos 
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated()]
        # Para list y retrieve (acciones de lectura)
        return [AllowAny()]

    def get_queryset(self):
        # Filtrar por elementos por eventos si se proporciona
        event_id = self.request.query_params.get('event', None)
        if event_id:
            items = Item.objects.filter(item_list__event_id=event_id)
            return items 
        return Item.objects.none()




