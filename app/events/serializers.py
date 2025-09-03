from rest_framework import serializers 
from django.contrib.auth.models import User 
from .models import Event, AudioNote, EventImage 
from app.item.serializers import ItemListSerializer 
from app.authentication.serializers import UserSerializer 
from app.item.models import ItemList 

class EventImageSerializer(serializers.ModelSerializer): 

    class Meta: 
        model = EventImage, 
        fields = ['id', 'image', 'caption', 'uploaded_at'] 
        read_only_fields = ['uploaded_at']

class AudioNoteSerializer(serializers.ModelSerializer): 

    class Meta: 
        model = AudioNote 
        fields = ['id', 'audio_file', 'title', 'uploaded_at']
        read_only_fields = ['recorded_at']

class EventSerializer(serializers.ModelSerializer): 

    organizer = UserSerializer(read_only=True) 
    organizer_id = serializers.PrimaryKeyRelatedField(
        queryset = User.objects.all(), 
        source = 'organizer', 
        write_only = True 
    )
    
    participants = UserSerializer(many=True, read_only=True) 
    participants_ids = serializers.PrimaryKeyRelatedField(
        queryset = User.objects.all(), 
        source = 'participants', 
        many=True,
        write_only = True, 
        required=False
    )

    images = EventImageSerializer(many=True, read_only=True)
    audio_notes = AudioNoteSerializer(many=True, read_only=True) 
    item_list = ItemListSerializer(read_only=True) 

    class Meta: 
        model = Event 
        fields = [
            'id', 'name', 'description', 'location', 'date', 'time', 'created_at', 'updated_at',
            'organizer', 'organizer_id', 'participants', 'participants_ids', 
            'images', 'audio_notes', 'item_list'
        ]

        read_only_fields = ['created_at', 'updated_at']

    def create(self, validated_data): 

        participants_data = validated_data.pop('participants', [])
        organizer = validated_data.pop('organizer')

        event = Event.objects.create(organizer=organizer, **validated_data)

        if participants_data: 
            event.participants.set(participants_data)

        ItemList.objects.create(event=event)

        return event




