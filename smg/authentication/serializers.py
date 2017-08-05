from rest_framework import serializers
from .models import User


class SignInSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)

    def validate(self, data):
        username = data['username']
        user = User.objects.filter(username=username).first()
        if user is None:
            raise serializers.ValidationError('User with username {} does not exist.'.format(username))
        data['user'] = user
        return data


class SelfDataSerializer(serializers.ModelSerializer):
    department = serializers.ReadOnlyField(source='department__name')

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'skype',
            'birthday',
            'employment_date',
            'first_name',
            'last_name',
            'patronymic',
            'education',
            'is_manager',
            'department',
            'token'
        )


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'skype',
            'birthday',
            'employment_date',
            'photo',
            'photo_large',
            'first_name',
            'last_name',
            'patronymic',
            'department',
            'is_manager',
        )
