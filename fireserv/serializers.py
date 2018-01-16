from django.contrib.auth.models import User
from rest_framework import serializers
from fireserv.models import Account

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'account')


class AccountSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='user.id')
    class Meta:
        model = Account
        fields = ('id', 'phonenum' 'fire_code', 'address', 'birthday', 'points', 'skin_type', 'skin_notes')

    def create(self, validated_data):
        return Account.objects.create(**validated_data)

    def update(self, validated_data):
        instance.phonenum = validated_data.get('phonenum', instance.phonenum)
        instance.fire_code = validated_data.get('fire_code', instance.fire_code)
        instance.address = validated_data.get('address', instance.address)
        instance.birthday = validated_data.get('birthday', instance.birthday)
        instance.points = validated_data.get('points', instance.points)
        skin_type = validated_data.get('skin_type', instance.skin_type)
        skin_notes = validated_data.get('skin_notes', instance.skin_notes)
        instance.save()
        return instance
