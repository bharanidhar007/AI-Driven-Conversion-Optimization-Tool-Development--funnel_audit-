from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Report, Profile
from django.contrib.auth.password_validation import validate_password

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    referral_code = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ('username','email','password','referral_code')

    def validate_password(self, value):
        # basic validation; adjust as needed
        validate_password(value)
        return value

    def create(self, validated_data):
        ref_code = validated_data.pop('referral_code', None)
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        # profile created by signal; handle referral
        if ref_code:
            try:
                ref_profile = Profile.objects.filter(referral_code=ref_code).first()
                if ref_profile:
                    user.profile.referred_by = ref_profile.user
                    user.profile.save()
                    # credit both
                    ref_profile.credits += 1
                    ref_profile.save()
                    user.profile.credits += 1
                    user.profile.save()
            except Exception:
                pass
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

class SubmitSerializer(serializers.Serializer):
    url = serializers.URLField()

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ['id','url','status','score','created_at','finished_at','error']

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['credits','referral_code','referred_by']
