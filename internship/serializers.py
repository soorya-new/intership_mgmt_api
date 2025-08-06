from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import User
from .models import Profile

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'role', 'phone']

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data.get('email'),
            role=validated_data.get('role'),
            phone=validated_data.get('phone')
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    

class ProfileSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='user.first_name', required=False)
    email = serializers.EmailField(source='user.email', required=False)

    class Meta:
        model = Profile
        fields = ['name', 'email', 'phone']

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        name = user_data.get('first_name')
        email = user_data.get('email')

        if name:
            instance.user.first_name = name
        if email:
            instance.user.email = email
        instance.user.save()

        instance.phone = validated_data.get('phone', instance.phone)
        instance.save()
        return instance
