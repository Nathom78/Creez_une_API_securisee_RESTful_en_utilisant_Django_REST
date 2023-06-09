from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from api_rest.models import (
    Users,
    Projects,
    Contributors,
    Issues,
    Comments
)


class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Users
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = Users.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class ProjetsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projects
        fields = ["title", "type", "pk"]


class ProjetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projects
        fields = '__all__'
        depth = 0


class ContributorsListSerializer(serializers.ModelSerializer):
    """
    User_id will be username
    """
    user = serializers.StringRelatedField()

    class Meta:
        model = Contributors
        fields = '__all__'


class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributors
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=Contributors.objects.all(),
                fields=['user', 'project']
            )
        ]


# assignee = serializers.PrimaryKeyRelatedField()
class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issues
        fields = '__all__'


class IssueListSerializer(serializers.ModelSerializer):
    project = serializers.StringRelatedField()

    class Meta:
        model = Issues
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = '__all__'


class CommentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ["issue", "pk"]
