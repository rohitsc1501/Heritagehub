"""Review serializers."""
from rest_framework import serializers
from .models import Review


class ReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()
    user_avatar = serializers.SerializerMethodField()
    place_name = serializers.CharField(source='place.place_name', read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'place', 'user', 'user_name', 'user_avatar', 'place_name',
                  'rating', 'review_text', 'review_date', 'created_at']
        read_only_fields = ['user', 'review_date', 'created_at']

    def get_user_name(self, obj):
        return obj.user.get_full_name() or obj.user.username

    def get_user_avatar(self, obj):
        if obj.user.avatar:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.user.avatar.url)
        return None

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
