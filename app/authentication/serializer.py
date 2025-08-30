from rest_framework import serializers
from django.contrib.auth.models import User 
from django.contrib.auth.password_validation import validate_password 
from django.contrib.auth.models import User 

class UserSerializer(serializers.ModelSerializer):

    class Meta: 
        model = User 
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']

class UserProfileSerializer(serializers.ModelSerializer):

    class Meta: 
        model = User 
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id', 'username', 'email']

class UserRegistrationSerializer(serializers.ModelSerializer): 
    
    password = serializers.CharField(
        write_only = True,
        required = True, 
        validators = [validate_password]
    )
    
    password2 = serializers.CharField(
        write_only = True,
        required = True, 
    )

    class Meta: 

        model = User 
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'password2']
        extra_kwargs = {
            'first_name' : {'required': False}, 
            'last_name' : {'required': False}, 
            'email' : {'required': True}
        }

    # Personalizamos la validación 
    def validate(self, attrs): 

        if attrs['password'] != attrs['password2']: 
            raise serializers.ValidationError({
                "password" : "Las contraseñas no coinciden"
            })

        if User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError({
                "email" : "Un usuario con este correo electrónico ya existe."
            })

        return attrs
    
    # Método personalizado para crear un usuario
    def create(self, validated_data):

        validated_data.pop('password2')

        user = User.objects.create_user(
            username = validated_data['username'], 
            email = validated_data['email'], 
            password = validated_data['password']
        )

        if 'first_name' in validated_data: 
            user.first_name = validated_data['first_name']
        if 'last_name' in validated_data:
            user.last_name = validated_data['last_name']

        user.save()
        return user
    
