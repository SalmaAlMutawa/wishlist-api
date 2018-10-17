from rest_framework import serializers
from items.models import Item, FavoriteItem
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['first_name', 'last_name',]

class FavoriteItemSerializer(serializers.ModelSerializer):
	user = UserSerializer()
	class Meta:
		model = FavoriteItem
		fields = ['user']

class ItemListSerializer(serializers.ModelSerializer):
	likes_count = serializers.SerializerMethodField()
	detail = serializers.HyperlinkedIdentityField(
		view_name = 'api-detail',
		lookup_field = "id",
		lookup_url_kwarg = "item_id"
		)
	added_by = UserSerializer()
	class Meta:
		model = Item
		exclude = ["image",]

	def get_likes_count(self, obj):
		return obj.favoriteitem_set.count()


class ItemDetailSerializer(serializers.ModelSerializer):
	liked_by = serializers.SerializerMethodField()
	class Meta:
		model = Item
		fields = "__all__"

	def get_liked_by(self, obj):
		likes = obj.favoriteitem_set.all()
		return FavoriteItemSerializer(likes, many=True).data