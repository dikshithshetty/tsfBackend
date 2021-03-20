from rest_framework import serializers
from .models import School, Student, Observation, Subscription, Transfer, UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for our user profil objects"""
    class Meta:
        model = UserProfile
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """Creates and returns a new user"""
        user = UserProfile(
            email = validated_data['email'],
            firstname = validated_data['firstname'],
            lastname = validated_data['lastname'],
            function = validated_data['function'],
            school = validated_data['school']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user

class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = '__all__'


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'


class ObservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Observation
        fields = '__all__'
        

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'

class TransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transfer
        fields = '__all__'


