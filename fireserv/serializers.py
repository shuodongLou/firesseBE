from django.contrib.auth.models import User
from rest_framework import serializers
from fireserv.models import Account
from rest_framework.validators import UniqueValidator

class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    class Meta:
        model = User
        fields = ('username', 'password')

    def create(self, validated_data):
        print("debug - validated_data: \n", validated_data)
        user = User(username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        return user

class AccountSerializer(serializers.ModelSerializer):

    user = serializers.IntegerField(source='user.id')
    phonenum = serializers.CharField(required=False, validators=[UniqueValidator(queryset=Account.objects.all())])

    class Meta:
        model = Account
        fields = ('user', 'phonenum', 'fire_code', 'address', 'birthday', 'points', 'skin_type', 'skin_notes')

    def create(self, validated_data):
        print("validated_data:")
        print(validated_data)
        data = {}
        data['user'] = User(id=validated_data['user']['id'])
        #data['phonenum'] = validated_data['phonenum']
        print(data)
        return Account.objects.create(**data)

    def update(self, instance, validated_data):
        instance.phonenum = validated_data.get('phonenum', instance.phonenum)
        instance.fire_code = validated_data.get('fire_code', instance.fire_code)
        instance.address = validated_data.get('address', instance.address)
        instance.birthday = validated_data.get('birthday', instance.birthday)
        instance.points = validated_data.get('points', instance.points)
        skin_type = validated_data.get('skin_type', instance.skin_type)
        skin_notes = validated_data.get('skin_notes', instance.skin_notes)
        instance.save()
        return instance
