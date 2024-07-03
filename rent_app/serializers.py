from rest_framework import serializers
from .models import RentRecord, User


class RentRecordListSerializer(serializers.ModelSerializer):
    user_rent = serializers.CharField(read_only=True)
    iha = serializers.CharField(read_only=True)
    class Meta:
        model = RentRecord
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username","email","password"]
    
    def create(self, validated_data):
        user = User(
            username=validated_data["username"],
            email=validated_data["email"]
        )
        user.set_password(validated_data["password"])
        user.save()
        return user