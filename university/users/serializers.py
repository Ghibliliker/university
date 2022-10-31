from rest_framework import serializers

from users.models import User


class CustomUserCreateSerializer(serializers.ModelSerializer):
    """Serializer for create or update users"""
    password = serializers.CharField(max_length=128, write_only=True, required=True)

    class Meta:
        model = User
        fields = (
            'username', 'password',
            'email', 'first_name',
            'last_name', 'gender', 'role'
        )

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for key, value in validated_data.items():
            setattr(instance, key, value)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class CustomUserSerializer(serializers.ModelSerializer):
    """Serializer for get users"""
    class Meta:
        model = User
        fields = (
            'username', 'id',
            'email', 'first_name',
            'last_name',
            'role', 'gender',
        )
