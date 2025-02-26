from .models import Keywords
from rest_framework import serializers


class KeywordsSerializer(serializers.ModelSerializer):
    keywords = serializers.ListField(child=serializers.CharField())

    class Meta:
        model = Keywords
        fields = '__all__'
