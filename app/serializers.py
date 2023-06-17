from django.db.models import F
from rest_framework import serializers
from .models import Task
from .validators import custom_title_validator


class TaskSerializer(serializers.ModelSerializer):
    title = serializers.CharField(validators=[custom_title_validator])

    def get_fields(self):
        fields = super().get_fields()
        request = self.context.get('request')
        if request and request.method == 'POST':
            fields['title'].required = True
        return fields

    def update(self, instance, validated_data):
        if 'title' in validated_data:
            instance.title = validated_data['title']
            instance.full_clean()
        return super().update(instance, validated_data)

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'created_at', 'status']


class TaskListSerializer(serializers.ModelSerializer):
    def update(self, instance, validated_data):
        if 'title' in validated_data:
            instance.title = validated_data['title']
            instance.full_clean()
        return super().update(instance, validated_data)

    class Meta:
        model = Task
        fields = ['title', 'created_at', 'status']
