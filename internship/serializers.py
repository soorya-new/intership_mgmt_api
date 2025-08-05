from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

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
