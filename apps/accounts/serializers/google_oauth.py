from rest_framework import serializers


class GoogleOAuthInputSerializer(serializers.Serializer):
    credential = serializers.CharField(required=True)
