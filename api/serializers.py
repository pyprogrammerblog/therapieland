from .models import TinyURL
from rest_framework import serializers


class TinyURLSerializer(serializers.ModelSerializer):

    class Meta:
        model = TinyURL
        fields = ('url', 'shortcode',)
        extra_kwargs = {'url': {'write_only': True}}


class URLStatsSerializer(serializers.Serializer):

    year = serializers.IntegerField()
    week = serializers.IntegerField()
    redirects_count = serializers.IntegerField(min_value=0)
