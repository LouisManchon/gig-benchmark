from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Serializer pour afficher les informations d'un utilisateur"""

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'role', 'created_at']
        read_only_fields = ['id', 'created_at', 'role']


class RegisterSerializer(serializers.ModelSerializer):
    """Serializer pour l'inscription d'un nouvel utilisateur"""

    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'},
        help_text="Minimum 8 characters"
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        help_text="Confirm password"
    )

    class Meta:
        model = User
        fields = ['username', 'password', 'password2', 'first_name', 'last_name']
        extra_kwargs = {
            'first_name': {'required': False},
            'last_name': {'required': False}
        }

    def validate_username(self, value):
        """Vérifier que le username est unique"""
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("This username already exists.")
        return value

    def validate(self, attrs):
        """Vérifier que les deux mots de passe correspondent"""
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({
                "password": "Passwords do not match."
            })
        return attrs

    def create(self, validated_data):
        """Créer un nouvel utilisateur"""
        # Retirer password2 (pas besoin de le sauvegarder)
        validated_data.pop('password2')

        # Créer l'utilisateur avec mot de passe hashé
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user


class LoginSerializer(serializers.Serializer):
    """Serializer pour la connexion d'un utilisateur"""

    username = serializers.CharField(
        required=True,
        help_text="Nom d'utilisateur"
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        help_text="Mot de passe"
    )
