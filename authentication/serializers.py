from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from authentication.models import User, Brands

class LoginSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)
        data['profile'] = LoginProfileSerializer(self.user).data

        return data
    
class LoginProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = (
            'password', 'last_login', 'is_active', 'is_superuser', 'is_staff',
            'groups', 'user_permissions', 'date_joined', 'created_at', 'updated_at',
            'is_deleted', 'deleted_at', 'created_by', 'updated_by', 'deleted_by'
        )
        
class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint.
    """
    model = User
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    
class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    class Meta:
        model = User
        fields = [
            'username', 'password', 'password2', 'email',
            'first_name', 'last_name', 'mobile', 'company_name',
            'address', 'brand_name', 'role',
        ]
        extra_kwargs = {
            'first_name' : {'required': True},
            'last_name' : {'required': True},
            'role': {'required': True},
            'mobile': {'required': True},
            'email': {'required': True},
        }
        
    def to_internal_value(self, data):
        brand_name = data.get('brand_name')
        if not Brands.objects.filter(name=brand_name).exists():
            name = Brands.objects.create(name= brand_name)
            name.save()
            
        brand_data = Brands.objects.filter(name= brand_name).first()
        data = {
            'username': data.get('username'),
            'password': data.get('password'),
            'password2': data.get('password2'),
            'email': data.get('email'),
            'first_name': data.get('first_name'),
            'last_name': data.get('last_name'),
            'role': data.get('role'),
            'company_name': data.get('company_name'),
            'address': data.get('address'),
            'brand_name': brand_data.id,
            'mobile': data.get('mobile'),
        }
        return super().to_internal_value(data)
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        
        return attrs
    
    def create(self, validated_data):
        user = User.objects.create(
            username= validated_data['username'],
            email= validated_data['email'],
            first_name= validated_data['first_name'],
            last_name= validated_data['last_name'],
            mobile= validated_data['mobile'],
            role= validated_data['role'],
            company_name= validated_data['company_name'],
            address= validated_data['address'],
            brand_name= validated_data['brand_name']
        )
        
        user.set_password(validated_data['password'])
        user.save()
        
        return user