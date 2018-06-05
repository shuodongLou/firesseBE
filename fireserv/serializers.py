from django.contrib.auth.models import User
from rest_framework import serializers
from fireserv.models import Account, Photo, Inquiry, Product, ProductImage, Agent, Order, Article, OrderProducts
from rest_framework.validators import UniqueValidator
from django.core.files.base import ContentFile
import base64
import six
import uuid
import imghdr

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
    role = serializers.CharField(required=True)

    class Meta:
        model = Account
        fields = ('user', 'username', 'role', 'fire_code', 'rec_code', 'province', 'city',
                'county', 'address', 'phone', 'name', 'sex','birthday', 'points',
                'skin_type', 'skin_notes')

    def create(self, validated_data):
        print("validated_data:")
        print(validated_data)
        data = {}
        data['user'] = User(id=validated_data['user']['id'])
        data['role'] = validated_data['role']
        data['phone'] = validated_data['phone']
        data['username'] = validated_data['phone']
        data['rec_code'] = validated_data['rec_code']
        data['fire_code'] = validated_data['fire_code']
        print(data)
        return Account.objects.create(**data)

    def update(self, instance, validated_data):
        print("in serializer update()")
        instance.role = validated_data.get('role', instance.role)
        instance.fire_code = validated_data.get('fire_code', instance.fire_code)
        instance.province = validated_data.get('province', instance.province)
        instance.city = validated_data.get('city', instance.city)
        instance.county = validated_data.get('county', instance.county)
        instance.address = validated_data.get('address', instance.address)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.name = validated_data.get('name', instance.name)
        instance.sex = validated_data.get('sex', instance.sex)
        instance.birthday = validated_data.get('birthday', instance.birthday)
        instance.points = validated_data.get('points', instance.points)
        skin_type = validated_data.get('skin_type', instance.skin_type)
        skin_notes = validated_data.get('skin_notes', instance.skin_notes)
        instance.save()
        return instance

class Base64ImageField(serializers.ImageField):

    def to_internal_value(self, data):
        # Check if this is a base64 string
        if isinstance(data, six.string_types):
            # Check if the base64 string is in the "data:" format
            if 'data:' in data and ';base64,' in data:
            	# Break out the header from the base64 content
                header, data = data.split(';base64,')


            # Try to decode the file. Return validation error if it fails.
            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail('invalid_image')

            # Generate file name:
            file_name = str(uuid.uuid4())[:12] # 12 characters are more than enough.
            # Get the file name extension:
            file_extension = self.get_file_extension(file_name, decoded_file)

            complete_file_name = "%s.%s" % (file_name, file_extension, )

            data = ContentFile(decoded_file, name=complete_file_name)

        return super(Base64ImageField, self).to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):
        def test_jpeg(h, f):
            """JPEG data in JFIF or Exif format"""
            if h[6:10] in (b'JFIF', b'Exif') or h[:2] == b'\xff\xd8':
                return 'jpeg'
        imghdr.tests.append(test_jpeg)
        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension

        return extension

class PhotoSerializer(serializers.ModelSerializer):

    account = serializers.IntegerField(source='account.id')
    photo = serializers.ListField(
        child = Base64ImageField(max_length=None, use_url=True)
    )
    inquiry_id = serializers.IntegerField(read_only=False)

    def create(self, validated_data):
        account = Account(id=validated_data['account']['id'])
        print('validated_data: ', validated_data)
        photo = validated_data['photo']
        print(validated_data)
        for item in photo:
            data = {}
            data['account'] = account
            data['photo'] = item
            data['inquiry_id'] = validated_data['inquiry_id']
            res = Photo.objects.create(**data)
        return res

    class Meta:
        model = Photo
        fields = ('account', 'photo', 'timestamp', 'inquiry_id')

class InquirySerializer(serializers.ModelSerializer):

    account = serializers.IntegerField(source='account.id')

    def create(self, validated_data):
        print('validated_data is : ', validated_data)
        print ('in create() - id: ', validated_data['account']['id'])
        account = Account(id=validated_data['account']['id'])
        data = {}
        data['account'] = account
        if 'note' in validated_data:
            data['note'] = validated_data['note']
        data['status'] = False
        return Inquiry.objects.create(**data)

    def update(self, instance, validated_data):
        print ('in update() validated_data: ', validated_data)
        instance.note = validated_data.get('note', instance.note)
        instance.status = validated_data.get('status', instance.status)
        instance.reply = validated_data.get('reply', instance.reply)
        instance.subtypea1 = validated_data.get('subtypea1', instance.subtypea1)
        instance.subtypea2 = validated_data.get('subtypea2', instance.subtypea2)
        instance.subtypea3 = validated_data.get('subtypea3', instance.subtypea3)
        instance.subtypeb1 = validated_data.get('subtypea1', instance.subtypeb1)
        instance.subtypeb2 = validated_data.get('subtypea2', instance.subtypeb2)
        instance.subtypeb3 = validated_data.get('subtypea3', instance.subtypeb3)
        instance.subtypec1 = validated_data.get('subtypea1', instance.subtypec1)
        instance.subtypec2 = validated_data.get('subtypea2', instance.subtypec2)
        instance.subtypec3 = validated_data.get('subtypea3', instance.subtypec3)
        instance.subtyped1 = validated_data.get('subtypea1', instance.subtyped1)
        instance.subtyped2 = validated_data.get('subtypea2', instance.subtyped2)
        instance.subtyped3 = validated_data.get('subtypea3', instance.subtyped3)
        instance.subtypee1 = validated_data.get('subtypea1', instance.subtypee1)
        instance.subtypee2 = validated_data.get('subtypea2', instance.subtypee2)
        instance.save()
        return instance

    class Meta:
        model = Inquiry
        fields = ('account', 'timestamp', 'note', 'status', 'reply', 'subtypea1',
                    'subtypea2', 'subtypea3', 'subtypeb1', 'subtypeb2', 'subtypeb3',
                    'subtypec1', 'subtypec2', 'subtypec3', 'subtyped1', 'subtyped2',
                    'subtyped3', 'subtypee1', 'subtypee2')

class ProductSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        return Product.objects.create(**validated_data)

    class Meta:
        model = Product
        fields = ('id', 'name', 'name_e', 'desc', 'series', 'status', 'price',
                  'inventory', 'histsales', 'volume', 'effects', 'ingredients',
                  'usage', 'notes')

class ProductImageSerializer(serializers.ModelSerializer):

    product = serializers.IntegerField(source='product.id')
    image = serializers.ListField(
        child = Base64ImageField(max_length=None, use_url=True)
    )

    def create(self, validated_data):
        product = Product(id=validated_data['product']['id'])
        print('validated_data: ', validated_data)
        image = validated_data['image']
        print(validated_data)
        for item in image:
            data = {}
            data['product'] = product
            data['image'] = item
            res = ProductImage.objects.create(**data)
        return res

    class Meta:
        model = ProductImage
        fields = ('product', 'image')

class AgentSerializer(serializers.ModelSerializer):
    fire_code = serializers.CharField(required=True, validators=[UniqueValidator(queryset=Agent.objects.all())])

    class Meta:
        model = Agent
        fields = ('id', 'acct_id', 'level', 'stars', 'commission_rate', 'fire_code',
                  'fire_points', 't_commission', 'y_commission', 'm_commission', 'status',
                  't_sales', 'y_sales', 'm_sales', 't_bonus', 'y_bonus', 'm_bonus')

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id', 'acct_id', 'time_created', 'time_delivered', 'time_resolved',
        'product_total', 'delivery_fee', 'final_payment', 'num_of_products', 'status',
        'fire_code', 'cus_name', 'cus_phone', 'cus_address', 'order_id')

class OrderProductsSerializer(serializers.ModelSerializer):

    order = serializers.IntegerField(source='order.id')
    product = serializers.ListField(
        child = serializers.CharField(max_length=100)
    )

    def create(self, validated_data):
        order = Order(id=validated_data['order']['id'])

        products = validated_data['product']
        for product in products:
            data = {
                'order': order,
                'product': product
            }
            res = OrderProducts.objects.create(**data)
        return res


    class Meta:
        model = OrderProducts
        fields = ('order', 'product')

class ArticleSerializer(serializers.ModelSerializer):

    cover = Base64ImageField(max_length=None, use_url=True, required=False)

    class Meta:
        model = Article
        fields = ('id', 'time_written', 'title', 'blurb', 'author', 'content', 'cover')
