from .models import Competition, Voice, Winner
from rest_framework import serializers


class VoiceSerializer(serializers.ModelSerializer):
    original_file = serializers.SerializerMethodField()
    converted_file = serializers.SerializerMethodField()
    state = serializers.SerializerMethodField()
    competition_id = serializers.SerializerMethodField()
    competition_name = serializers.SerializerMethodField()

    class Meta:
        model = Voice
        fields = (
            'id',
            'creation_date',
            'author_firstname',
            'author_lastname',
            'author_email',
            'observations',
            'original_file',
            'converted_file',
            'state',
            'competition_id',
            'competition_name',
        )

    @classmethod
    def get_original_file(self, obj):
        try:
            return obj.original_file.url
        except:
            return None

    @classmethod
    def get_converted_file(self, obj):
        try:
            return obj.converted_file.url
        except:
            return None

    @classmethod
    def get_state(self, obj):
        try:
            return obj.get_state_display()
        except:
            return None

    @classmethod
    def get_competition_id(self, obj):
        try:
            return obj.competition.id
        except:
            return None

    @classmethod
    def get_competition_name(self, obj):
        try:
            return obj.competition.name
        except:
            return None


class VoiceUploadSerializer(serializers.ModelSerializer):
    original_file = serializers.FileField(max_length=None, use_url=True)

    class Meta:
        model = Voice
        fields = (
            'id',
            'creation_date',
            'author_firstname',
            'author_lastname',
            'author_email',
            'observations',
            'original_file',
            'state',
            'competition',
        )


class CompetitionSerializer(serializers.ModelSerializer):
    banner = serializers.SerializerMethodField()

    class Meta:
        model = Competition
        fields = (
            'id',
            'name',
            'banner',
            'url',
            'start_date',
            'end_date',
            'amount',
            'text',
            'recommendations',
            'owner',
        )

    @classmethod
    def get_banner(self, obj):
        try:
            return obj.banner.url
        except:
            return None


class WinnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Winner
        fields = (
            'competition',
            'voice',
        )


class CompetitionUploadSerializer(serializers.ModelSerializer):
    banner = serializers.ImageField(max_length=None, use_url=True,
                                    required=False)

    class Meta:
        model = Competition
        fields = (
            'name',
            'banner',
            'url',
            'start_date',
            'end_date',
            'amount',
            'text',
            'recommendations',
            'owner',
        )
