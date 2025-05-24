from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'username', 'name', 'age', 'gender', 'phone')

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
            name=validated_data.get('name'),
            age=validated_data.get('age'),
            gender=validated_data.get('gender'),
            phone=validated_data.get('phone'),
        )
        user.set_password(validated_data['password'])
        user.save()
        return user