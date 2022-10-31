from rest_framework import serializers

from faculty.models import Subject, Group, Direction
from users.serializers import CustomUserSerializer


class SubjectSerializer(serializers.ModelSerializer):
    """Serializer for subjects"""
    class Meta:
        model = Subject
        fields = ('name',)


class DirectionSerializer(serializers.ModelSerializer):
    """Serializer for get/list directions"""
    subjects = SubjectSerializer(many=True)
    curator = CustomUserSerializer()

    class Meta:
        model = Direction
        fields = ('name', 'curator', 'subjects')


class DirectionCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for create/update directions"""
    subjects = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Subject.objects.all()
    )

    class Meta:
        model = Direction
        fields = ('name', 'curator', 'subjects')

    def create_subjects(self, subjects, direction):
        for subject in subjects:
            direction.subjects.add(subject)

    def create(self, validated_data):
        subjects = validated_data.pop('subjects')
        direction = Direction.objects.create(**validated_data)
        self.create_subjects(subjects, direction)
        return direction

    def update(self, instance, validated_data):
        subjects_list = validated_data.pop('subjects', instance.subjects)
        instance.subjects.clear()
        self.create_subjects(subjects_list, instance)
        instance.save()
        return super().update(instance, validated_data)


class GroupSerializer(serializers.ModelSerializer):
    """Serializer for get/list groups"""
    students = CustomUserSerializer(many=True)

    class Meta:
        model = Group
        fields = ('name', 'direction', 'students')


class GroupCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for create/update groups"""

    class Meta:
        model = Group
        fields = ('name', 'direction')
